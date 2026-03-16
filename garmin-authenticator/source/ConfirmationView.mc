// Microsoft Authenticator number matching confirmation view
// Shows 3 numbers - user must select the correct one to approve login
// Supports both number matching and simple approve/deny

using Toybox.WatchUi;
using Toybox.Graphics;
using Toybox.Lang;
using Toybox.Timer;
using Toybox.Math;

class ConfirmationView extends WatchUi.View {

    private var _serviceName as String = "";
    private var _correctNumber as Number = 0;
    private var _options as Array<Number> = [0, 0, 0];
    private var _selectedIndex as Number = 0;
    private var _timeoutSeconds as Number = 60;
    private var _timer as Timer.Timer?;
    private var _callback as Method?;

    // Initialize with the correct number from Microsoft's login screen
    function initialize(serviceName as String, correctNumber as Number, callback as Method?) {
        View.initialize();
        _serviceName = serviceName;
        _correctNumber = correctNumber;
        _callback = callback;
        generateOptions();
    }

    // Generate 3 options: the correct number + 2 random decoys
    function generateOptions() as Void {
        var options = new [3];
        // Place the correct answer at a random position
        var correctPos = (Math.rand() % 3).abs();

        for (var i = 0; i < 3; i++) {
            if (i == correctPos) {
                options[i] = _correctNumber;
            } else {
                // Generate a random 2-digit number (10-99) different from correct
                var decoy = _correctNumber;
                while (decoy == _correctNumber || arrayContains(options, decoy, i)) {
                    decoy = 10 + (Math.rand() % 90).abs();
                }
                options[i] = decoy;
            }
        }
        _options = options;
    }

    // Helper: check if value exists in array up to index
    function arrayContains(arr as Array<Number>, val as Number, upTo as Number) as Boolean {
        for (var i = 0; i < upTo; i++) {
            if (arr[i] == val) {
                return true;
            }
        }
        return false;
    }

    function onShow() as Void {
        _timer = new Timer.Timer();
        _timer.start(method(:onTimerTick), 1000, true);
    }

    function onHide() as Void {
        if (_timer != null) {
            _timer.stop();
            _timer = null;
        }
    }

    function onTimerTick() as Void {
        _timeoutSeconds--;
        if (_timeoutSeconds <= 0) {
            handleSelection(-1);  // Timeout = deny
        }
        WatchUi.requestUpdate();
    }

    function onUpdate(dc as Graphics.Dc) as Void {
        var width = dc.getWidth();
        var height = dc.getHeight();
        var centerX = width / 2;
        var centerY = height / 2;

        // Clear screen
        dc.setColor(Graphics.COLOR_BLACK, Graphics.COLOR_BLACK);
        dc.clear();

        // Microsoft logo indicator (blue bar at top)
        dc.setColor(0x0078D4, Graphics.COLOR_TRANSPARENT);  // Microsoft blue
        dc.fillRectangle(centerX - 40, 8, 80, 4);

        // Header
        dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_TRANSPARENT);
        dc.drawText(centerX, centerY - 70, Graphics.FONT_SMALL,
                    "Inloggen goedkeuren?",
                    Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        // Service/account name
        dc.setColor(Graphics.COLOR_LT_GRAY, Graphics.COLOR_TRANSPARENT);
        dc.drawText(centerX, centerY - 48, Graphics.FONT_XTINY,
                    _serviceName,
                    Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        // Instruction
        dc.setColor(Graphics.COLOR_YELLOW, Graphics.COLOR_TRANSPARENT);
        dc.drawText(centerX, centerY - 28, Graphics.FONT_XTINY,
                    "Kies het juiste nummer:",
                    Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        // Draw the 3 number options as large buttons
        var buttonWidth = 70;
        var buttonHeight = 50;
        var spacing = 8;
        var totalWidth = 3 * buttonWidth + 2 * spacing;
        var startX = centerX - totalWidth / 2;
        var buttonY = centerY + 2;

        for (var i = 0; i < 3; i++) {
            var bx = startX + i * (buttonWidth + spacing);
            var by = buttonY;

            if (i == _selectedIndex) {
                // Selected button: highlighted with border
                dc.setColor(0x0078D4, Graphics.COLOR_TRANSPARENT);  // Microsoft blue
                dc.fillRoundedRectangle(bx, by, buttonWidth, buttonHeight, 8);
                dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_TRANSPARENT);
            } else {
                // Unselected button: outline only
                dc.setColor(Graphics.COLOR_DK_GRAY, Graphics.COLOR_TRANSPARENT);
                dc.fillRoundedRectangle(bx, by, buttonWidth, buttonHeight, 8);
                dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_TRANSPARENT);
            }

            // Draw number
            dc.drawText(bx + buttonWidth / 2, by + buttonHeight / 2,
                        Graphics.FONT_NUMBER_MILD,
                        _options[i].toString(),
                        Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);
        }

        // Draw deny option at bottom
        dc.setColor(Graphics.COLOR_DK_RED, Graphics.COLOR_TRANSPARENT);
        dc.drawText(centerX, centerY + 70, Graphics.FONT_XTINY,
                    "Weigeren (terug-knop)",
                    Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        // Timeout indicator
        var timeColor = (_timeoutSeconds <= 10) ? Graphics.COLOR_RED : Graphics.COLOR_DK_GRAY;
        dc.setColor(timeColor, Graphics.COLOR_TRANSPARENT);
        dc.drawText(centerX, height - 15, Graphics.FONT_XTINY,
                    _timeoutSeconds + "s",
                    Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);

        // Timeout progress arc
        var arcRadius = (width < height ? width : height) / 2 - 4;
        var progress = _timeoutSeconds.toFloat() / 60.0;
        var arcDegrees = (progress * 360).toNumber();

        dc.setPenWidth(3);
        dc.setColor(Graphics.COLOR_DK_GRAY, Graphics.COLOR_TRANSPARENT);
        dc.drawArc(centerX, centerY, arcRadius, Graphics.ARC_CLOCKWISE, 90, 90 - 360);
        dc.setColor(timeColor, Graphics.COLOR_TRANSPARENT);
        dc.drawArc(centerX, centerY, arcRadius, Graphics.ARC_CLOCKWISE, 90, 90 - arcDegrees);
    }

    // Move selection left
    function selectPrevious() as Void {
        _selectedIndex = (_selectedIndex + 2) % 3;
        WatchUi.requestUpdate();
    }

    // Move selection right
    function selectNext() as Void {
        _selectedIndex = (_selectedIndex + 1) % 3;
        WatchUi.requestUpdate();
    }

    // Confirm current selection
    function confirmSelection() as Void {
        handleSelection(_options[_selectedIndex]);
    }

    // Deny (back button)
    function denyRequest() as Void {
        handleSelection(-1);
    }

    function handleSelection(selectedNumber as Number) as Void {
        if (_timer != null) {
            _timer.stop();
            _timer = null;
        }

        var approved = (selectedNumber == _correctNumber);

        if (_callback != null) {
            _callback.invoke(approved);
        }

        WatchUi.switchToView(
            new ResultView(approved),
            new ResultDelegate(),
            WatchUi.SLIDE_UP
        );
    }

    function getSelectedIndex() as Number {
        return _selectedIndex;
    }
}

// Confirmation delegate for handling button presses
class ConfirmationDelegate extends WatchUi.BehaviorDelegate {

    private var _view as ConfirmationView;

    function initialize(view as ConfirmationView) {
        BehaviorDelegate.initialize();
        _view = view;
    }

    // Up/Previous button: move selection left
    function onPreviousPage() as Boolean {
        _view.selectPrevious();
        return true;
    }

    // Down/Next button: move selection right
    function onNextPage() as Boolean {
        _view.selectNext();
        return true;
    }

    // Select/Enter button: confirm selection
    function onSelect() as Boolean {
        _view.confirmSelection();
        return true;
    }

    // Back button: deny the request
    function onBack() as Boolean {
        _view.denyRequest();
        return true;
    }
}

// Brief result screen after approve/deny
class ResultView extends WatchUi.View {

    private var _approved as Boolean;
    private var _timer as Timer.Timer?;

    function initialize(approved as Boolean) {
        View.initialize();
        _approved = approved;
    }

    function onShow() as Void {
        _timer = new Timer.Timer();
        _timer.start(method(:onTimeout), 2000, false);
    }

    function onHide() as Void {
        if (_timer != null) {
            _timer.stop();
            _timer = null;
        }
    }

    function onTimeout() as Void {
        WatchUi.popView(WatchUi.SLIDE_DOWN);
    }

    function onUpdate(dc as Graphics.Dc) as Void {
        var width = dc.getWidth();
        var height = dc.getHeight();
        var centerX = width / 2;
        var centerY = height / 2;

        dc.setColor(Graphics.COLOR_BLACK, Graphics.COLOR_BLACK);
        dc.clear();

        if (_approved) {
            // Large checkmark
            dc.setColor(Graphics.COLOR_GREEN, Graphics.COLOR_TRANSPARENT);
            dc.setPenWidth(5);
            dc.drawLine(centerX - 25, centerY - 5, centerX - 8, centerY + 15);
            dc.drawLine(centerX - 8, centerY + 15, centerX + 30, centerY - 20);

            dc.drawText(centerX, centerY + 40, Graphics.FONT_MEDIUM,
                        "Bevestigd",
                        Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);
        } else {
            // Large X mark
            dc.setColor(Graphics.COLOR_RED, Graphics.COLOR_TRANSPARENT);
            dc.setPenWidth(5);
            dc.drawLine(centerX - 20, centerY - 20, centerX + 20, centerY + 20);
            dc.drawLine(centerX + 20, centerY - 20, centerX - 20, centerY + 20);

            dc.drawText(centerX, centerY + 40, Graphics.FONT_MEDIUM,
                        "Geweigerd",
                        Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);
        }
    }
}

class ResultDelegate extends WatchUi.BehaviorDelegate {

    function initialize() {
        BehaviorDelegate.initialize();
    }

    function onBack() as Boolean {
        WatchUi.popView(WatchUi.SLIDE_DOWN);
        return true;
    }
}
