import requests
import binascii

payload = "79d17b1653402c3ed9e7c9f328c58c4e2349521c269aed602c67d9a3411a50b2ac4ba2a3e50d2980fc6c25ae94d3aa5741b37d3ad9ab6a5b297ba61620da4670d0d0a604f18ce31b6fba63762c3ddc279d38d021848850317ab37ca078fc5e9558f9bcd01f58c4e3e1764f9fc3993675d28a6b62aa202d13560e96e607fa4c32ae77853072eedc5e6e1be0bfb57458a51799749a09597132095f59b4310cadb6d6c2532d87c5b6968a397b6dd1da88989096dbef0f95f0deb67541fe9ed84891c388ec622195be1f95a9434417835e1f32b059542e936c9c1e4e242b6493980bd601cb91ac8714a02580175d885065c92964aa415a9f6f7ea4a8994629944109c911daf27c4090f7f02d278fa9186b611de1d6ef61d6c3d2445fe2e6a902278d6d652194a30cef66db989abba931bc8268ea7ae97a24d46be0ce28c225aaaecb1ce3c88f986a2934f7cbc5a90f0463f0669d01a6e8b57faea3d781323e31c549c648ac562095eb12a09c64be592c51f5c1841504365786713f50098f1e9150b230ea8e57262ac0ff3f604f4b3c2220d95d1813beed36af0949c0e26f173d69146ee712fef20c27cbfab71429c1debf7b68076a712c2eacb05d735e13cd3ec161972a761e41e7530b60122aa4b32d80f1486e94c636fcdd22b5dcad999cde7d7ad42904c6f93aca27dd41686b508c95a5daefd6907b01098178a038f39e8f4ee0dd2530626b5afb571980d13cb76b2fd0ddd1b288b14ae356c631d859bf90165f10618b54dbacc2b192c11db77b03980996014614d230016c86f03c7ea706037678f879f6d87c1d5e2948640fea80fdef10a42b410c8f1353d0e933202cb74e32d3a8c78b55de9b21a26c6d75387a43e8f51568ecbda06cc7110492bad59585be936355f05632a32d0d66a0014a8f6982bc60025f1cd2766deaf2c40b94879fcaf0fd14b0493eb334bc142c646ce009178cc865fa33eaf7827063da92a05b57b121ee24e8a8438855aa1cf532b42de3e802fa0fbb55fb5a04c7d3e66e576e3d4b6002063e868e2415530b250dfaaa6143e20b19a6d01fbe40c92a2091e2cd637130be49bdb3e71a7d90dcb367a8d70bb71fde1b1da62ef025314db08d1fc0cdd4e161b7596ad4aaef35b2a06597eb805621054667948d893046f40741cda382105031cc6e5cbfbcb7315dbbaa82b2a1bb0409b62a27dcb316d65026066a6aa75093bc64d5d0103c72e7f225a1f062bf5e704ff9cfd0d60a2dd14495301e66648287fb10cf0b2b9f09500b2abb340d1b1516444ec17d2dbe0fc016b14a124ae9929a529af9f58a2ae33cf7a59bfde8be63"

def send(ct):
    url = "http://localhost:4242/api"
    data = {
        'c': binascii.hexlify(ct)
    }
    r = requests.get(url, params=data)
    return r.status_code == 200

data = binascii.unhexlify(payload)

def xor_byte_at(block, pos, x):
  return block[:pos] + chr(ord(block[pos])^x) + block[pos+1:]

second_last = data[-32:-16]
last = data[-16:]

guesses = [0] + range(2, 256) + [1]

plaintext = "";

for x in range(16):
  attempt = second_last + last

  # Neutralize with plaintext
  for i, plain_byte in enumerate(reversed(plaintext)):
    attempt = xor_byte_at(attempt, 16-1-i, ord(plain_byte))

  # xor with valid padding
  for i in xrange(x + 1):
    attempt = xor_byte_at(attempt, 16-1-i, x+1)

  # xor with guess
  for guess in guesses:
    if send(xor_byte_at(attempt, 16-1-i, guess)):
      plaintext = chr(guess) + plaintext
      break

  print repr(plaintext)
