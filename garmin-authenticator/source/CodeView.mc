// Main TOTP code display view
// Shows the current 6-digit code with a countdown timer arc

using Toybox.WatchUi;
using Toybox.Graphics;
using Toybox.Timer;
using Toybox.Lang;

class CodeView extends WatchUi.View {

    private var _accountName as String = "";
    private var _secret as String = "";
    private var _currentCode as String = "------";
    private var _secondsRemaining as Number = 30;
    private var _timer as Timer.Timer?;
    private var _accountIndex as Number = 0;
    private var _totalAccounts as Number = 0;

    function initialize(accountName as String, secret as String,
                        accountIndex as Number, totalAccounts as Number) {
        View.initialize();
        _accountName = accountName;
        _secret = secret;
        _accountIndex = accountIndex;
        _totalAccounts = totalAccounts;
    }

    function onLayout(dc as Graphics.Dc) as Void {
        updateCode();
    }

    function onShow() as Void {
        // Update code every second
        _timer = new Timer.Timer();
        _timer.start(method(:onTimerTick), 1000, true);
        updateCode();
    }

    function onHide() as Void {
        if (_timer != null) {
            _timer.stop();
            _timer = null;
        }
    }

    function onTimerTick() as Void {
        updateCode();
        WatchUi.requestUpdate();
    }

    function updateCode() as Void {
        _currentCode = TotpGenerator.generate(_secret);
        _secondsRemaining = TotpGenerator.getSecondsRemaining();
    }

    function onUpdate(dc as Graphics.Dc) as Void {
        var width = dc.getWidth();
        var height = dc.getHeight();
        var centerX = width / 2;
        var centerY = height / 2;

        // Clear screen
        dc.setColor(Graphics.COLOR_BLACK, Graphics.COLOR_BLACK);
        dc.clear();

        // Draw countdown arc (circular progress indicator)
        var arcRadius = (width < height ? width : height) / 2 - 8;
        var progress = _secondsRemaining.toFloat() / 30.0;
        var arcDegrees = (progress * 360).toNumber();

        // Background arc (dark gray)
        dc.setColor(Graphics.COLOR_DK_GRAY, Graphics.COLOR_TRANSPARENT);
        dc.setPenWidth(4);
        dc.drawArc(centerX, centerY, arcRadius, Graphics.ARC_CLOCKWISE, 90, 90 - 360);

        // Progress arc (color changes based on time remaining)
        if (_secondsRemaining <= 5) {
            dc.setColor(Graphics.COLOR_RED, Graphics.COLOR_TRANSPARENT);
        } else if (_secondsRemaining <= 10) {
            dc.setColor(Graphics.COLOR_YELLOW, Graphics.COLOR_TRANSPARENT);
        } else {
            dc.setColor(Graphics.COLOR_GREEN, Graphics.COLOR_TRANSPARENT);
        }
        dc.drawArc(centerX, centerY, arcRadius, Graphics.ARC_CLOCKWISE, 90, 90 - arcDegrees);

        // Draw account name
        dc.setColor(Graphics.COLOR_LT_GRAY, Graphics.COLOR_TRANSPARENT);
        dc.drawText(centerX, centerY - 45, Graphics.FONT_SMALL,
                    _accountName, Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        // Draw TOTP code (formatted as "123 456")
        var formattedCode = _currentCode.substring(0, 3) + " " + _currentCode.substring(3, 6);
        dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_TRANSPARENT);
        dc.drawText(centerX, centerY, Graphics.FONT_NUMBER_HOT,
                    formattedCode, Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        // Draw seconds remaining
        dc.setColor(Graphics.COLOR_YELLOW, Graphics.COLOR_TRANSPARENT);
        dc.drawText(centerX, centerY + 45, Graphics.FONT_SMALL,
                    _secondsRemaining + "s",
                    Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        // Draw page indicator dots if multiple accounts
        if (_totalAccounts > 1) {
            drawPageIndicator(dc, centerX, height - 20, _accountIndex, _totalAccounts);
        }
    }

    // Draw small dots indicating which account is shown
    function drawPageIndicator(dc as Graphics.Dc, x as Number, y as Number,
                               current as Number, total as Number) as Void {
        var dotSpacing = 12;
        var startX = x - ((total - 1) * dotSpacing / 2);

        for (var i = 0; i < total; i++) {
            if (i == current) {
                dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_TRANSPARENT);
                dc.fillCircle(startX + i * dotSpacing, y, 3);
            } else {
                dc.setColor(Graphics.COLOR_DK_GRAY, Graphics.COLOR_TRANSPARENT);
                dc.fillCircle(startX + i * dotSpacing, y, 2);
            }
        }
    }

    function getAccountIndex() as Number {
        return _accountIndex;
    }

    function getTotalAccounts() as Number {
        return _totalAccounts;
    }

    function getSecret() as String {
        return _secret;
    }

    function getAccountName() as String {
        return _accountName;
    }
}
