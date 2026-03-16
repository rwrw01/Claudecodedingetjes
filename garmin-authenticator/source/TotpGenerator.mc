// TOTP (Time-based One-Time Password) generator - RFC 6238
// Generates 6-digit codes compatible with Google Authenticator, Authy, etc.

using Toybox.Lang;
using Toybox.Time;

module TotpGenerator {

    const TIME_STEP = 30;  // Standard 30-second time step
    const CODE_DIGITS = 6;

    // Generate a TOTP code from a Base32-encoded secret
    function generate(base32Secret as String) as String {
        var secret = Base32.decode(base32Secret);
        return generateFromBytes(secret);
    }

    // Generate a TOTP code from a raw byte array secret
    function generateFromBytes(secret as Array<Number>) as String {
        var timeCounter = getTimeCounter();
        var timeBytes = counterToBytes(timeCounter);

        // Compute HMAC-SHA1
        var hmacResult = Sha1.hmac(secret, timeBytes);

        // Dynamic truncation (RFC 4226 section 5.4)
        var offset = hmacResult[19] & 0x0F;
        var code = ((hmacResult[offset] & 0x7F) << 24) |
                   ((hmacResult[offset + 1] & 0xFF) << 16) |
                   ((hmacResult[offset + 2] & 0xFF) << 8) |
                   (hmacResult[offset + 3] & 0xFF);

        // Modulo to get desired number of digits
        var modulo = 1;
        for (var i = 0; i < CODE_DIGITS; i++) {
            modulo *= 10;
        }
        code = code % modulo;

        // Format with leading zeros
        return padCode(code);
    }

    // Get current time counter (Unix time / TIME_STEP)
    function getTimeCounter() as Number {
        var now = Time.now();
        return now.value() / TIME_STEP;
    }

    // Get seconds remaining in current time step
    function getSecondsRemaining() as Number {
        var now = Time.now();
        return TIME_STEP - (now.value() % TIME_STEP);
    }

    // Convert counter to 8-byte big-endian array
    function counterToBytes(counter as Number) as Array<Number> {
        var bytes = new [8];
        bytes[0] = 0;
        bytes[1] = 0;
        bytes[2] = 0;
        bytes[3] = 0;
        bytes[4] = (counter >> 24) & 0xFF;
        bytes[5] = (counter >> 16) & 0xFF;
        bytes[6] = (counter >> 8) & 0xFF;
        bytes[7] = counter & 0xFF;
        return bytes;
    }

    // Pad code with leading zeros to CODE_DIGITS length
    function padCode(code as Number) as String {
        var result = code.toString();
        while (result.length() < CODE_DIGITS) {
            result = "0" + result;
        }
        return result;
    }
}
