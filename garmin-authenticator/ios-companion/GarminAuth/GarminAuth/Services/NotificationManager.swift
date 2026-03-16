// Notification Manager
// Beheert lokale notificaties en verwerkt inkomende push notificaties
//
// Let op: iOS staat niet toe om notificaties van andere apps (zoals Microsoft
// Authenticator) te onderscheppen. Daarom werkt deze app als handmatige brug:
// de gebruiker voert het nummer in dat op het inlogscherm staat.

import Foundation
import UserNotifications

class NotificationManager: ObservableObject {

    @Published var hasPermission = false
    @Published var pendingNumber: Int?

    // Vraag notificatie-toestemming
    func requestPermission() {
        UNUserNotificationCenter.current().requestAuthorization(
            options: [.alert, .sound, .badge]
        ) { [weak self] granted, error in
            DispatchQueue.main.async {
                self?.hasPermission = granted
            }

            if let error = error {
                print("Notificatie-fout: \(error.localizedDescription)")
            }
        }
    }

    // Stuur een lokale notificatie als herinnering
    func sendLocalNotification(title: String, body: String) {
        guard hasPermission else { return }

        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default

        let request = UNNotificationRequest(
            identifier: UUID().uuidString,
            content: content,
            trigger: nil  // Direct versturen
        )

        UNUserNotificationCenter.current().add(request)
    }

    // Stuur bevestigingsnotificatie
    func sendApprovalNotification(approved: Bool) {
        let title = approved ? "Inloggen bevestigd" : "Inloggen geweigerd"
        let body = approved
            ? "Je hebt het inlogverzoek goedgekeurd via je Garmin horloge."
            : "Je hebt het inlogverzoek geweigerd via je Garmin horloge."

        sendLocalNotification(title: title, body: body)
    }
}
