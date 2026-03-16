// Input delegate for the TOTP code view
// Handles swipe/button navigation between accounts

using Toybox.WatchUi;
using Toybox.Lang;

class CodeDelegate extends WatchUi.BehaviorDelegate {

    private var _view as CodeView;
    private var _store as AccountStore;

    function initialize(view as CodeView, store as AccountStore) {
        BehaviorDelegate.initialize();
        _view = view;
        _store = store;
    }

    // Swipe up / next page: go to next account
    function onNextPage() as Boolean {
        var accounts = _store.getAccounts();
        var total = accounts.size();
        if (total <= 1) {
            return false;
        }
        var nextIndex = (_view.getAccountIndex() + 1) % total;
        var account = accounts[nextIndex];
        WatchUi.switchToView(
            new CodeView(account[:name], account[:secret], nextIndex, total),
            new CodeDelegate(
                new CodeView(account[:name], account[:secret], nextIndex, total),
                _store
            ),
            WatchUi.SLIDE_UP
        );
        return true;
    }

    // Swipe down / previous page: go to previous account
    function onPreviousPage() as Boolean {
        var accounts = _store.getAccounts();
        var total = accounts.size();
        if (total <= 1) {
            return false;
        }
        var prevIndex = (_view.getAccountIndex() + total - 1) % total;
        var account = accounts[prevIndex];
        WatchUi.switchToView(
            new CodeView(account[:name], account[:secret], prevIndex, total),
            new CodeDelegate(
                new CodeView(account[:name], account[:secret], prevIndex, total),
                _store
            ),
            WatchUi.SLIDE_DOWN
        );
        return true;
    }

    // Back button: exit app
    function onBack() as Boolean {
        WatchUi.popView(WatchUi.SLIDE_RIGHT);
        return true;
    }
}
