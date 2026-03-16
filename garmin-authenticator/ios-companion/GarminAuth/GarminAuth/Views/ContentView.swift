// Hoofdscherm van de companion app
// Toont verbindingsstatus en biedt toegang tot nummer-invoer en geschiedenis

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var garminManager: GarminManager
    @EnvironmentObject var notificationManager: NotificationManager
    @State private var showAuthInput = false

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Verbindingsstatus header
                ConnectionStatusBar()

                ScrollView {
                    VStack(spacing: 24) {
                        // Hoofdknop: nieuw verzoek bevestigen
                        SendToWatchButton(showAuthInput: $showAuthInput)

                        // Laatste reactie van horloge
                        if let response = garminManager.lastResponse {
                            LastResponseCard(response: response)
                        }

                        // Uitleg
                        HowItWorksCard()
                    }
                    .padding()
                }
            }
            .navigationTitle("Garmin Auth")
            .sheet(isPresented: $showAuthInput) {
                NumberInputView()
            }
        }
    }
}

// MARK: - Verbindingsstatus balk

struct ConnectionStatusBar: View {
    @EnvironmentObject var garminManager: GarminManager

    var body: some View {
        HStack {
            Circle()
                .fill(garminManager.isConnected ? Color.green : Color.red)
                .frame(width: 10, height: 10)

            Text(garminManager.connectionStatus.rawValue)
                .font(.caption)
                .foregroundColor(.secondary)

            Spacer()

            if garminManager.isConnected {
                Image(systemName: "applewatch.watchface")
                    .foregroundColor(.blue)
                Text(garminManager.deviceName)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.horizontal)
        .padding(.vertical, 8)
        .background(Color(.systemGray6))
    }
}

// MARK: - Hoofdknop

struct SendToWatchButton: View {
    @EnvironmentObject var garminManager: GarminManager
    @Binding var showAuthInput: Bool

    var body: some View {
        Button(action: { showAuthInput = true }) {
            VStack(spacing: 12) {
                Image(systemName: "lock.shield.fill")
                    .font(.system(size: 48))
                    .foregroundColor(.white)

                Text("Inloggen bevestigen")
                    .font(.title2)
                    .fontWeight(.semibold)
                    .foregroundColor(.white)

                Text("Voer het nummer in van je scherm")
                    .font(.subheadline)
                    .foregroundColor(.white.opacity(0.8))
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 32)
            .background(
                LinearGradient(
                    colors: [Color(red: 0, green: 0.47, blue: 0.83),  // Microsoft blauw
                             Color(red: 0, green: 0.35, blue: 0.7)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            )
            .cornerRadius(16)
            .shadow(color: .blue.opacity(0.3), radius: 8, y: 4)
        }
        .disabled(!garminManager.isConnected)
        .opacity(garminManager.isConnected ? 1.0 : 0.5)
    }
}

// MARK: - Laatste reactie kaart

struct LastResponseCard: View {
    let response: AuthResponse

    var body: some View {
        HStack {
            Image(systemName: response.approved ? "checkmark.circle.fill" : "xmark.circle.fill")
                .font(.title2)
                .foregroundColor(response.approved ? .green : .red)

            VStack(alignment: .leading) {
                Text(response.statusText)
                    .font(.headline)

                Text(response.timestamp, style: .relative)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    + Text(" geleden")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Spacer()
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

// MARK: - Uitleg kaart

struct HowItWorksCard: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Hoe werkt het?")
                .font(.headline)

            StepRow(number: 1, text: "Je logt ergens in met Microsoft account")
            StepRow(number: 2, text: "Er verschijnt een 2-cijferig nummer op je scherm")
            StepRow(number: 3, text: "Open deze app en voer het nummer in")
            StepRow(number: 4, text: "Kies het juiste nummer op je Garmin horloge")
            StepRow(number: 5, text: "Inloggen is bevestigd!")
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

struct StepRow: View {
    let number: Int
    let text: String

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Text("\(number)")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundColor(.white)
                .frame(width: 22, height: 22)
                .background(Color.blue)
                .clipShape(Circle())

            Text(text)
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
    }
}
