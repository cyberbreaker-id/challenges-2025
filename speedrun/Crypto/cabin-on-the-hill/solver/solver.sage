ciphertext = "RRVXGQYTDXYKPDTLHNPJTZAKREIWNHFWUSOLZYCNYBXJNMPTKFLPALGGPAQTGRONBLCLKGUDYTHFUJMMAINZVHIWNXGO"
knownCiphertext = [(ord(c) - ord('A')) for c in ciphertext[:8] + ciphertext[-16:-8]]
knownPlaintext1 = [(ord(c) - ord('A')) for c in "WARNINGI"]
knownPlaintext2 = [(ord(c) - ord('A')) for c in "PEATDONT"]

knownPlaintext = knownPlaintext1 + knownPlaintext2
R = IntegerModRing(26)
M = MatrixSpace(R,4,4)
M_C = M(knownCiphertext).transpose()
M_P = M(knownPlaintext).transpose()

K = M(M_C * M_P.inverse())
K = K.transpose()

H = HillCryptosystem(AlphabeticStrings(), 4)
print(H.deciphering(K, H.encoding(ciphertext)))