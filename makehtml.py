import os
BASE_DIR = os.path.dirname(__file__)

import pystache

def templating(html, data):
	response = pystache.render(html, data)
	return response

def exploteStrings(string):
	estring = u""
	for i, c in enumerate(string):
		if i %50 == 0:
			estring += c+"\n"
		else:
			estring += c
	return estring

import xmltodict

def extracdata(xml):
	doc = xmltodict.parse(open(xml,"r"))
	cfdi = doc["cfdi:Comprobante"]
	#datos generales
	fecha = cfdi["@fecha"]
	LugarExpedicion = cfdi["@LugarExpedicion"]
	tipoDeComprobante = cfdi["@tipoDeComprobante"]
	formaDePago = cfdi["@formaDePago"]
	subTotal = cfdi["@subTotal"]
	total = cfdi["@total"]
	folio = cfdi["cfdi:Complemento"]["tfd:TimbreFiscalDigital"]["@UUID"]
	#emisor
	if cfdi["cfdi:Emisor"].has_key("@nombre"):
		nombreEmisor = cfdi["cfdi:Emisor"]["@nombre"]
	else:
		nombreEmisor = u""
	rfcEmisor = cfdi["cfdi:Emisor"]["@rfc"]
	#receptor
	if cfdi["cfdi:Receptor"].has_key("@nombre"):
		nombreReceptor = cfdi["cfdi:Receptor"]["@nombre"]
	else:
		nombreReceptor = u""
	rfcReceptor = cfdi["cfdi:Receptor"]["@rfc"]
	#pie
	sello = exploteStrings(cfdi["cfdi:Complemento"]["tfd:TimbreFiscalDigital"]["@selloCFD"])
	certificado = exploteStrings(cfdi["cfdi:Complemento"]["tfd:TimbreFiscalDigital"]["@selloSAT"])
	noSAT = cfdi["cfdi:Complemento"]["tfd:TimbreFiscalDigital"]["@noCertificadoSAT"]
	FechaTimbrado = cfdi["cfdi:Complemento"]["tfd:TimbreFiscalDigital"]["@FechaTimbrado"]

	return {
		"fecha": fecha,
		"LugarExpedicion": LugarExpedicion,
		"tipoDeComprobante": tipoDeComprobante,
		"formaDePago": formaDePago,
		"folio": folio,
		"subTotal": subTotal,
		"total": total,
		"nombreEmisor": nombreEmisor,
		"rfcEmisor": rfcEmisor,
		"nombreReceptor": nombreReceptor,
		"rfcReceptor": rfcReceptor,
		"conceptos": cfdi["cfdi:Conceptos"],
		"impuestos": cfdi["cfdi:Impuestos"],
		"sello": sello,
		"certificado": certificado,
		"noSAT": noSAT,
		"FechaTimbrado": FechaTimbrado,
	}


from makepdf import convertHtmlToPdf

def main(arg):
	for i, xml in enumerate(arg):
		data = extracdata(xml)
		html = templating(open(BASE_DIR+"/template.html","r+").read(), data)
		outputFilename = "factura "+str(i)+".pdf"
		convertHtmlToPdf(html,outputFilename)

if __name__ == '__main__':
	import sys
	if len(sys.argv[1:]) > 0:
		main(sys.argv[1:])
	else:
		raw_input("no hay archivos xml")