// Garmin Authenticator - iOS Companion App
// Stuurt Microsoft Authenticator number matching verzoeken naar je Garmin horloge
//
// Werking:
// 1. Je krijgt een Microsoft login-verzoek op je PC
// 2. Open deze app en voer het 2-cijferige nummer in dat op je scherm staat
// 3. Het nummer wordt naar je Garmin horloge gestuurd
// 4. Kies het juiste nummer op je horloge om in te loggen

import SwiftUI
import UserNotifications

@main
struct GarminAuthApp: App {
    @StateObject private var garminManager = GarminManager()
    @StateObject private var notificationManager = NotificationManager()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(garminManager)
                .environmentObject(notificationManager)
                .onAppear {
                    notificationManager.requestPermission()
                    garminManager.connect()
                }
        }
    }
}
