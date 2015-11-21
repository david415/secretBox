
import scrypt
import nacl.secret
import nacl.utils
import nacl.hash
import nacl.encoding
import getpass
import binascii
import re


def encryptFile(filename, key):
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    plaintext_fh = open(filename, 'r')
    plaintext = plaintext_fh.read()
    plaintext_fh.close()
    box = nacl.secret.SecretBox(key)
    return box.encrypt(plaintext, nonce, encoder=nacl.encoding.Base64Encoder)

def promptlyEncryptFile(filename):
    """
    Encrypt file and return ciphertext.
    Prompt twice to set a passphrase/key.
    """
    passphrase = getpass.getpass("Enter passphrase:")
    passphrase2 = getpass.getpass("Enter passphrase:")
    if passphrase != passphrase2:
        print "passphrases don't match"
        return None

    key = hashPassphrase(passphrase)
    return encryptFile(filename, key)

def decryptFile(filename, key):
    # XXX obviously for big ass files this will not work
    fh = open(filename, 'r')
    bin_ciphertext = binascii.a2b_base64(fh.read())
    fh.close()
    nonce = bin_ciphertext[0:24]
    ciphertext = bin_ciphertext[24:]
    box = nacl.secret.SecretBox(key)
    return box.decrypt(ciphertext, nonce)

def promptlyDecryptFile(filename):
    """
    Decrypt file and return plaintext.
    Prompt for the passphrase.
    """
    passphrase = getpass.getpass("Enter passphrase:")
    key = hashPassphrase(passphrase)
    return decryptFile(filename, key)

def hashPassphrase(passphrase):
    not_stretched = nacl.hash.sha256(passphrase, encoder=nacl.encoding.RawEncoder)
    salt = not_stretched[:10] # XXX

    # XXX sufficiently paranoid?
    return scrypt.hash(not_stretched, salt, p=1000, r=20, N=2048, buflen=32)

