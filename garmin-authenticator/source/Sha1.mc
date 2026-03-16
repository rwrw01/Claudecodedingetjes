// SHA-1 implementation for Garmin Connect IQ (Monkey C)
// Used by HMAC-SHA1 for TOTP code generation

using Toybox.Lang;

module Sha1 {

    // SHA-1 constants
    const BLOCK_SIZE = 64;
    const DIGEST_SIZE = 20;

    // Initial hash values
    function initialHash() as Array<Number> {
        return [
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476,
            0xC3D2E1F0
        ];
    }

    // Left rotate 32-bit integer
    function leftRotate(n as Number, bits as Number) as Number {
        return ((n << bits) | (n >>> (32 - bits))) & 0xFFFFFFFF;
    }

    // Compute SHA-1 hash of a byte array
    function hash(message as Array<Number>) as Array<Number> {
        var msgLen = message.size();

        // Pre-processing: add padding
        var padded = new [0];
        for (var i = 0; i < msgLen; i++) {
            padded.add(message[i]);
        }

        // Append bit '1' (0x80)
        padded.add(0x80);

        // Append zeros until message length ≡ 56 (mod 64)
        while (padded.size() % 64 != 56) {
            padded.add(0x00);
        }

        // Append original message length in bits as 64-bit big-endian
        var bitLen = msgLen * 8;
        // High 32 bits (for messages < 512MB, high word is 0)
        padded.add(0x00);
        padded.add(0x00);
        padded.add(0x00);
        padded.add(0x00);
        // Low 32 bits
        padded.add((bitLen >> 24) & 0xFF);
        padded.add((bitLen >> 16) & 0xFF);
        padded.add((bitLen >> 8) & 0xFF);
        padded.add(bitLen & 0xFF);

        // Initialize hash values
        var h = initialHash();

        // Process each 64-byte block
        var numBlocks = padded.size() / 64;
        for (var block = 0; block < numBlocks; block++) {
            var offset = block * 64;

            // Prepare message schedule (80 words)
            var w = new [80];
            for (var i = 0; i < 16; i++) {
                var idx = offset + i * 4;
                w[i] = ((padded[idx] & 0xFF) << 24) |
                        ((padded[idx + 1] & 0xFF) << 16) |
                        ((padded[idx + 2] & 0xFF) << 8) |
                        (padded[idx + 3] & 0xFF);
            }
            for (var i = 16; i < 80; i++) {
                w[i] = leftRotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1);
            }

            // Initialize working variables
            var a = h[0];
            var b = h[1];
            var c = h[2];
            var d = h[3];
            var e = h[4];

            // Main loop
            for (var i = 0; i < 80; i++) {
                var f;
                var k;
                if (i < 20) {
                    f = (b & c) | ((~b) & d);
                    k = 0x5A827999;
                } else if (i < 40) {
                    f = b ^ c ^ d;
                    k = 0x6ED9EBA1;
                } else if (i < 60) {
                    f = (b & c) | (b & d) | (c & d);
                    k = 0x8F1BBCDC;
                } else {
                    f = b ^ c ^ d;
                    k = 0xCA62C1D6;
                }

                var temp = (leftRotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF;
                e = d;
                d = c;
                c = leftRotate(b, 30);
                b = a;
                a = temp;
            }

            // Update hash values
            h[0] = (h[0] + a) & 0xFFFFFFFF;
            h[1] = (h[1] + b) & 0xFFFFFFFF;
            h[2] = (h[2] + c) & 0xFFFFFFFF;
            h[3] = (h[3] + d) & 0xFFFFFFFF;
            h[4] = (h[4] + e) & 0xFFFFFFFF;
        }

        // Produce the final hash as byte array
        var digest = new [DIGEST_SIZE];
        for (var i = 0; i < 5; i++) {
            digest[i * 4] = (h[i] >> 24) & 0xFF;
            digest[i * 4 + 1] = (h[i] >> 16) & 0xFF;
            digest[i * 4 + 2] = (h[i] >> 8) & 0xFF;
            digest[i * 4 + 3] = h[i] & 0xFF;
        }

        return digest;
    }

    // Compute HMAC-SHA1
    function hmac(key as Array<Number>, message as Array<Number>) as Array<Number> {
        var blockKey = new [BLOCK_SIZE];

        // If key is longer than block size, hash it first
        var actualKey = key;
        if (actualKey.size() > BLOCK_SIZE) {
            actualKey = hash(actualKey);
        }

        // Zero-pad key to block size
        for (var i = 0; i < BLOCK_SIZE; i++) {
            if (i < actualKey.size()) {
                blockKey[i] = actualKey[i];
            } else {
                blockKey[i] = 0x00;
            }
        }

        // Create inner and outer padded keys
        var ipad = new [BLOCK_SIZE];
        var opad = new [BLOCK_SIZE];
        for (var i = 0; i < BLOCK_SIZE; i++) {
            ipad[i] = blockKey[i] ^ 0x36;
            opad[i] = blockKey[i] ^ 0x5C;
        }

        // Inner hash: SHA1(ipad || message)
        var innerMsg = new [0];
        for (var i = 0; i < BLOCK_SIZE; i++) {
            innerMsg.add(ipad[i]);
        }
        for (var i = 0; i < message.size(); i++) {
            innerMsg.add(message[i]);
        }
        var innerHash = hash(innerMsg);

        // Outer hash: SHA1(opad || inner_hash)
        var outerMsg = new [0];
        for (var i = 0; i < BLOCK_SIZE; i++) {
            outerMsg.add(opad[i]);
        }
        for (var i = 0; i < DIGEST_SIZE; i++) {
            outerMsg.add(innerHash[i]);
        }

        return hash(outerMsg);
    }
}
