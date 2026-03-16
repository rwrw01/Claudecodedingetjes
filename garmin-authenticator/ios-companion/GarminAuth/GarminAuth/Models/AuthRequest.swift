// Model voor een authenticatieverzoek

import Foundation

struct AuthRequest: Identifiable, Codable {
    let id: UUID
    let serviceName: String
    let number: Int
    let timestamp: Date
    var status: AuthStatus

    init(serviceName: String, number: Int) {
        self.id = UUID()
        self.serviceName = serviceName
        self.number = number
        self.timestamp = Date()
        self.status = .pending
    }

    enum AuthStatus: String, Codable {
        case pending = "Wachtend"
        case approved = "Bevestigd"
        case denied = "Geweigerd"
        case expired = "Verlopen"

        var color: String {
            switch self {
            case .pending: return "yellow"
            case .approved: return "green"
            case .denied: return "red"
            case .expired: return "gray"
            }
        }
    }
}

// Bericht dat naar het Garmin horloge wordt gestuurd
struct WatchMessage: Codable {
    let type: String
    let service: String
    let number: Int

    init(request: AuthRequest) {
        self.type = "ms_auth"
        self.service = request.serviceName
        self.number = request.number
    }

    func toDictionary() -> [String: Any] {
        return [
            "type": type,
            "service": service,
            "number": number
        ]
    }
}
