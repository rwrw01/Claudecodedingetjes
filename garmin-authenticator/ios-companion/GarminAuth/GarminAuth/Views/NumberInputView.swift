// Nummer invoer scherm
// Hier voert de gebruiker het 2-cijferige nummer in dat Microsoft toont op het inlogscherm
// Het nummer wordt dan naar het Garmin horloge gestuurd voor bevestiging

import SwiftUI

struct NumberInputView: View {
    @EnvironmentObject var garminManager: GarminManager
    @EnvironmentObject var notificationManager: NotificationManager
    @Environment(\.dismiss) var dismiss

    @State private var enteredNumber = ""
    @State private var serviceName = "Microsoft"
    @State private var isSending = false
    @State private var sendResult: SendResult?

    enum SendResult {
        case success
        case failure
    }

    var body: some View {
        NavigationStack {
            VStack(spacing: 32) {
                // Header
                VStack(spacing: 8) {
                    Image(systemName: "number.circle.fill")
                        .font(.system(size: 60))
                        .foregroundColor(.blue)

                    Text("Welk nummer zie je?")
                        .font(.title2)
                        .fontWeight(.bold)

                    Text("Voer het 2-cijferige nummer in dat\nop je inlogscherm staat")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                }
                .padding(.top, 20)

                // Service naam veld
                VStack(alignment: .leading, spacing: 6) {
                    Text("Service")
                        .font(.caption)
                        .foregroundColor(.secondary)

                    TextField("Bijv. Microsoft, Google", text: $serviceName)
                        .textFieldStyle(.roundedBorder)
                }
                .padding(.horizontal)

                // Nummer invoer
                VStack(spacing: 16) {
                    Text(displayNumber)
                        .font(.system(size: 72, weight: .bold, design: .rounded))
                        .foregroundColor(enteredNumber.isEmpty ? .gray.opacity(0.3) : .primary)
                        .frame(height: 90)

                    // Numpad
                    LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 3), spacing: 12) {
                        ForEach(1...9, id: \.self) { digit in
                            NumpadButton(digit: "\(digit)") {
                                appendDigit("\(digit)")
                            }
                        }

                        // Lege cel
                        Color.clear.frame(height: 60)

                        NumpadButton(digit: "0") {
                            appendDigit("0")
                        }

                        // Wis knop
                        Button(action: deleteDigit) {
                            Image(systemName: "delete.left.fill")
                                .font(.title2)
                                .foregroundColor(.red)
                                .frame(width: 60, height: 60)
                        }
                    }
                    .padding(.horizontal, 40)
                }

                // Verstuur knop
                Button(action: sendToWatch) {
                    HStack {
                        if isSending {
                            ProgressView()
                                .tint(.white)
                        } else {
                            Image(systemName: "applewatch")
                            Text("Verstuur naar horloge")
                        }
                    }
                    .font(.headline)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(canSend ? Color.blue : Color.gray)
                    .cornerRadius(14)
                }
                .disabled(!canSend || isSending)
                .padding(.horizontal)

                Spacer()
            }
            .navigationTitle("Nummer invoeren")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Annuleer") { dismiss() }
                }
            }
            .alert("Verstuurd!", isPresented: showSuccessAlert) {
                Button("OK") { dismiss() }
            } message: {
                Text("Het nummer is naar je Garmin horloge gestuurd.\nKies het juiste nummer op je horloge om in te loggen.")
            }
            .alert("Fout", isPresented: showFailureAlert) {
                Button("Probeer opnieuw", role: .cancel) {}
            } message: {
                Text("Kan het nummer niet versturen. Controleer of je horloge verbonden is.")
            }
        }
    }

    // MARK: - Computed Properties

    private var displayNumber: String {
        if enteredNumber.isEmpty {
            return "--"
        } else if enteredNumber.count == 1 {
            return "0\(enteredNumber)"
        }
        return enteredNumber
    }

    private var canSend: Bool {
        return enteredNumber.count == 2 && garminManager.isConnected
    }

    private var showSuccessAlert: Binding<Bool> {
        Binding(
            get: { sendResult == .success },
            set: { if !$0 { sendResult = nil } }
        )
    }

    private var showFailureAlert: Binding<Bool> {
        Binding(
            get: { sendResult == .failure },
            set: { if !$0 { sendResult = nil } }
        )
    }

    // MARK: - Actions

    private func appendDigit(_ digit: String) {
        guard enteredNumber.count < 2 else { return }
        enteredNumber += digit
    }

    private func deleteDigit() {
        guard !enteredNumber.isEmpty else { return }
        enteredNumber.removeLast()
    }

    private func sendToWatch() {
        guard let number = Int(enteredNumber) else { return }

        isSending = true

        let request = AuthRequest(serviceName: serviceName, number: number)

        garminManager.sendAuthRequest(request) { success in
            isSending = false
            sendResult = success ? .success : .failure

            if success {
                notificationManager.sendLocalNotification(
                    title: "Verzoek verstuurd",
                    body: "Kies nummer \(number) op je Garmin horloge"
                )
            }
        }
    }
}

// MARK: - Numpad knop

struct NumpadButton: View {
    let digit: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(digit)
                .font(.system(size: 28, weight: .medium, design: .rounded))
                .frame(width: 60, height: 60)
                .background(Color(.systemGray5))
                .cornerRadius(30)
        }
        .foregroundColor(.primary)
    }
}
