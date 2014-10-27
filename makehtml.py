import xmltodict

import pystache
def templating(html, data):
	response = pystache.render(html, data)
	return response

def extracdata():
	doc = xmltodict.parse(open("./18D20955-1C03-484D-8481-FBB931927D75.xml","r"))
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
	nombreEmisor = cfdi["cfdi:Emisor"]["@nombre"]
	rfcEmisor = cfdi["cfdi:Emisor"]["@rfc"]
	#receptor
	nombreReceptor = cfdi["cfdi:Receptor"]["@nombre"]
	rfcReceptor = cfdi["cfdi:Receptor"]["@rfc"]
	#print "cfdi:Conceptos: " + str(cfdi["cfdi:Conceptos"])
	#print "cfdi:Impuestos: " + str(cfdi["cfdi:Impuestos"])

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
		"impuestos": cfdi["cfdi:Impuestos"]
	}


from makepdf import convertHtmlToPdf

def main():
	data = extracdata()
	html = templating(open("./template.html","r+").read(), data)
	outputFilename = "test.pdf"
	convertHtmlToPdf(html,outputFilename)

if __name__ == '__main__':
	main()