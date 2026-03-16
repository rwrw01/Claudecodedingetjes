// Account storage manager
// Stores authenticator accounts (name + Base32 secret) in Garmin Application.Storage

using Toybox.Application;
using Toybox.Lang;

class AccountStore {

    const MAX_ACCOUNTS = 10;
    const STORAGE_KEY_COUNT = "account_count";
    const STORAGE_KEY_PREFIX_NAME = "account_name_";
    const STORAGE_KEY_PREFIX_SECRET = "account_secret_";

    // Load all stored accounts as array of {:name, :secret} dictionaries
    function getAccounts() as Array<Dictionary> {
        var count = getAccountCount();
        var accounts = new [0];

        for (var i = 0; i < count; i++) {
            var name = Application.Storage.getValue(STORAGE_KEY_PREFIX_NAME + i);
            var secret = Application.Storage.getValue(STORAGE_KEY_PREFIX_SECRET + i);
            if (name != null && secret != null) {
                accounts.add({:name => name, :secret => secret});
            }
        }

        return accounts;
    }

    // Get the number of stored accounts
    function getAccountCount() as Number {
        var count = Application.Storage.getValue(STORAGE_KEY_COUNT);
        if (count == null) {
            return 0;
        }
        return count as Number;
    }

    // Add a new account
    function addAccount(name as String, base32Secret as String) as Boolean {
        var count = getAccountCount();
        if (count >= MAX_ACCOUNTS) {
            return false;
        }

        Application.Storage.setValue(STORAGE_KEY_PREFIX_NAME + count, name);
        Application.Storage.setValue(STORAGE_KEY_PREFIX_SECRET + count, base32Secret);
        Application.Storage.setValue(STORAGE_KEY_COUNT, count + 1);
        return true;
    }

    // Remove an account by index
    function removeAccount(index as Number) as Void {
        var count = getAccountCount();
        if (index < 0 || index >= count) {
            return;
        }

        // Shift remaining accounts down
        for (var i = index; i < count - 1; i++) {
            var nextName = Application.Storage.getValue(STORAGE_KEY_PREFIX_NAME + (i + 1));
            var nextSecret = Application.Storage.getValue(STORAGE_KEY_PREFIX_SECRET + (i + 1));
            Application.Storage.setValue(STORAGE_KEY_PREFIX_NAME + i, nextName);
            Application.Storage.setValue(STORAGE_KEY_PREFIX_SECRET + i, nextSecret);
        }

        // Remove last entry
        Application.Storage.deleteValue(STORAGE_KEY_PREFIX_NAME + (count - 1));
        Application.Storage.deleteValue(STORAGE_KEY_PREFIX_SECRET + (count - 1));
        Application.Storage.setValue(STORAGE_KEY_COUNT, count - 1);
    }

    // Check if any accounts exist
    function hasAccounts() as Boolean {
        return getAccountCount() > 0;
    }
}
