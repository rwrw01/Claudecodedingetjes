// Garmin Authenticator - Main Application
// TOTP code generator + Microsoft Authenticator number matching
//
// Features:
// - Generate 6-digit TOTP codes (compatible with Google/Microsoft Authenticator)
// - Microsoft number matching: select the correct 2-digit number to approve login
// - Multiple accounts with swipe navigation
// - Visual countdown timer with color-coded urgency
// - Accounts stored securely in Garmin Application.Storage
//
// Usage:
// 1. Add accounts via Garmin Connect Mobile app (settings)
// 2. Open app on watch to see TOTP codes
// 3. When a Microsoft login request comes in, the number matching
//    screen appears - select the correct number shown on your PC/phone

using Toybox.Application;
using Toybox.WatchUi;
using Toybox.Lang;
using Toybox.System;
using Toybox.Communications;

class AuthenticatorApp extends Application.AppBase {

    private var _store as AccountStore?;

    function initialize() {
        AppBase.initialize();
    }

    function onStart(state as Dictionary?) as Void {
        _store = new AccountStore();

        // Register for phone communication (for receiving push auth requests)
        Communications.registerForPhoneAppMessages(method(:onPhoneMessage));
    }

    function getInitialView() as Array<WatchUi.Views or WatchUi.InputDelegates>? {
        _store = new AccountStore();

        if (_store.hasAccounts()) {
            var accounts = _store.getAccounts();
            var firstAccount = accounts[0];
            var view = new CodeView(
                firstAccount[:name],
                firstAccount[:secret],
                0,
                accounts.size()
            );
            return [view, new CodeDelegate(view, _store)] as Array<WatchUi.Views or WatchUi.InputDelegates>;
        } else {
            // No accounts: show setup instructions
            return [new NoAccountsView(), new NoAccountsDelegate()] as Array<WatchUi.Views or WatchUi.InputDelegates>;
        }
    }

    // Handle incoming messages from the companion phone app
    // Used for Microsoft Authenticator number matching push notifications
    function onPhoneMessage(msg as Communications.PhoneAppMessage) as Void {
        var data = msg.data;

        if (data instanceof Dictionary) {
            var type = data["type"];

            if (type != null && type.equals("ms_auth")) {
                // Microsoft Authenticator number matching request
                var service = data["service"];
                var number = data["number"];

                if (service != null && number != null) {
                    var confirmView = new ConfirmationView(
                        service as String,
                        number as Number,
                        method(:onAuthResponse)
                    );
                    WatchUi.pushView(
                        confirmView,
                        new ConfirmationDelegate(confirmView),
                        WatchUi.SLIDE_UP
                    );
                }
            }
        }
    }

    // Callback when user approves or denies authentication
    function onAuthResponse(approved as Boolean) as Void {
        // Send response back to phone companion app
        var response = {
            "type" => "ms_auth_response",
            "approved" => approved
        };

        Communications.transmit(response, null, new CommListener());
    }

    // Handle settings changes from Garmin Connect Mobile
    function onSettingsChanged() as Void {
        // Reload accounts when settings are changed via phone
        var numAccounts = Application.Properties.getValue("num_accounts");
        if (numAccounts != null && numAccounts instanceof Number) {
            _store = new AccountStore();

            for (var i = 0; i < numAccounts; i++) {
                var name = Application.Properties.getValue("account_name_" + i);
                var secret = Application.Properties.getValue("account_secret_" + i);
                if (name != null && secret != null) {
                    _store.addAccount(name as String, secret as String);
                }
            }
        }
    }

    function onStop(state as Dictionary?) as Void {
    }
}

// Communication listener for transmit callbacks
class CommListener extends Communications.ConnectionListener {

    function initialize() {
        ConnectionListener.initialize();
    }

    function onComplete() as Void {
        System.println("Auth response sent successfully");
    }

    function onError() as Void {
        System.println("Failed to send auth response");
    }
}

// View shown when no accounts are configured
class NoAccountsView extends WatchUi.View {

    function initialize() {
        View.initialize();
    }

    function onUpdate(dc as Graphics.Dc) as Void {
        var width = dc.getWidth();
        var height = dc.getHeight();
        var centerX = width / 2;
        var centerY = height / 2;

        dc.setColor(Graphics.COLOR_BLACK, Graphics.COLOR_BLACK);
        dc.clear();

        // Lock icon (simple representation)
        dc.setColor(0x0078D4, Graphics.COLOR_TRANSPARENT);
        dc.setPenWidth(3);
        dc.drawArc(centerX, centerY - 45, 15, Graphics.ARC_CLOCKWISE, 0, 180);
        dc.fillRoundedRectangle(centerX - 18, centerY - 45, 36, 25, 4);

        // Title
        dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_TRANSPARENT);
        dc.drawText(centerX, centerY - 10, Graphics.FONT_SMALL,
                    "Authenticator",
                    Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        // Instructions
        dc.setColor(Graphics.COLOR_LT_GRAY, Graphics.COLOR_TRANSPARENT);
        dc.drawText(centerX, centerY + 15, Graphics.FONT_XTINY,
                    "Geen accounts",
                    Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        dc.drawText(centerX, centerY + 35, Graphics.FONT_XTINY,
                    "Voeg toe via",
                    Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        dc.drawText(centerX, centerY + 50, Graphics.FONT_XTINY,
                    "Garmin Connect app",
                    Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);
    }
}

class NoAccountsDelegate extends WatchUi.BehaviorDelegate {

    function initialize() {
        BehaviorDelegate.initialize();
    }

    function onBack() as Boolean {
        System.exit();
        return true;
    }
}
