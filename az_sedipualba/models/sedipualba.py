# -*- coding: utf-8 -*-
#License: Copyright Rolan Benavent Talens. All rights reserved.

from datetime import datetime, timezone
from hashlib import sha256
import base64
import requests
import xmltodict

class Sedipualba:

	#############################################################################
	### Constructor
	### username: Sedipualba username
	### password: Sedipualba password
	### entity: Sedipualba entity
	### mode: Sedipualba mode (pre- or None)
	#############################################################################
	def __init__(self, username:str, password:str, entity:str, mode:str):
		
		self.username = username
		self.password = password
		self.entity = entity
		self.mode = mode

		self._xml = (
			'<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
				'<soap:Body>'
					'<$FUNCTION$ xmlns="$XMLNS$">'
						'<$wsseg_user$>$USERNAME$</$wsseg_user$>'
						'<$wsseg_pass$>$WSSEGPASS$</$wsseg_pass$>'
						'$pk_entidad$'
						'$PARAMETERS$'
					'</$FUNCTION$>'
				'</soap:Body>'
			'</soap:Envelope>'
		)

		self._url = {
			'sefycu': {
				'api': 'https://$MODE$$ENTITY$.sedipualba.es/sefycu/wssefycu.asmx?wsdl',
				'xmlns': 'https://eadmin.dipualba.es/sefycu/wssefycu.asmx'
			},
			'segra': {
				'api': 'https://$MODE$$ENTITY$.sedipualba.es/sefycu/wssegra.asmx?wsdl',
				'xmlns': 'https://eadmin.dipualba.es/sefycu/wssegra.asmx'
			},
			'segex': {
				'api': 'https://$MODE$$ENTITY$.sedipualba.es/segex/wssegex.asmx?wsdl',
				'xmlns': 'https://eadmin.dipualba.es/segex/wssegex.asmx'
			},
			'seres_registro': {
				'api': 'https://$MODE$$ENTITY$.sedipualba.es/seres/Servicios/wsseresregistro.asmx?wsdl',
				'xmlns': 'http://sedipualba.es/wsSeresV1.2'
			},
			'seres_ciudadano': {
				'api': 'https://$MODE$$ENTITY$.sedipualba.es/wsdirectorio.asmx?wsdl',
				'xmlns': 'http://sedipualba.es/wsSeresV1'
			},
			'directorio': {
				'api': 'https://$MODE$$ENTITY$.sedipualba.es/wsdirectorio.asmx?wsdl',
				'xmlns': 'https://sedipualba.es/wsdirectorio.asmx'
			},
			'sello': {
				'api': 'https://$MODE$$ENTITY$.sedipualba.es/firma/wsselloelectronico.asmx?wsdl',
				'xmlns': 'http://www.sedipualba.es/firma/WSSelloElectronico.asmx'
			},
			'notificaciones': {
				'api': 'https://$MODE$$ENTITY$.sedipualba.es/sefycu/wsnotificaciones.asmx',
				'xmlns': '/admin/'
			}
		}

		self._headers = {
			'Content-Type': 'text/xml; charset=utf-8'
		}

		self.func_params = {}

	#############################################################################
	### Generates function with same name as api
	### api: API name
	### args: Arguments
	#############################################################################
	def __getattr__(self, name):
		def function(api, **args):
			return self.callAPI(api = api, func = name, 
				params = (args['params'] if 'params' in args else args), 
				mapParams = (args['mapParams'] if 'mapParams' in args else {}))
		return function

	#############################################################################
	### Initializes function parameters from API
	### api: API name
	#############################################################################
	def __setFuncParams(self, api):
		authKeys = {
			'user': ['wsSegUser', 'wsseg_user'], 
			'pass': ['wsSegPass', 'wsseg_pass'], 
			'entity': ['idEntidad', 'pk_entidad', 'pkEntidad']
		}
		response = requests.get(self._url[api]['api'].replace('$ENTITY$', self.entity).replace('$MODE$', 'pre-' if self.mode else '')).text
		result = xmltodict.parse(response)['wsdl:definitions']['wsdl:types']['s:schema']['s:element']
		
		for res in result:
			if not res['@name'].strip().endswith('Response'):
				func = res['@name'].strip()
				if not func in self.func_params:
					# Adds function parameters if doesn't exist
					self.func_params[func] = self.__initFunc()

				if res['s:complexType'] and res['s:complexType']['s:sequence']['s:element']:
					for element in res['s:complexType']['s:sequence']['s:element']:
						auth = False
						for key in authKeys:
							if element['@name'].strip() in authKeys[key]:
								self.func_params[func][key] = element['@name'].strip()
								auth = True
								break
						if not auth and element['@minOccurs'] == "0":
							self.func_params[func]['params']['optional'].append( element['@name'].strip() )
						elif not auth:
							self.func_params[func]['params']['required'].append( element['@name'].strip() )
				
			else:
				func = res['@name'].strip()[0:-8]
				if not func in self.func_params:
					# Adds function parameters if doesn't exist
					self.func_params[func] = self.__initFunc()
				# Adds function response
				if not res['@name'].strip() in self.func_params[func]['response']:
					self.func_params[func]['response'].append( res['@name'].strip() )

				if res['s:complexType'] and res['s:complexType']['s:sequence']['s:element']['@name']:
					# Adds response result, if returns anything
					if not res['s:complexType']['s:sequence']['s:element']['@name'].strip() in self.func_params[func]['response']:
						self.func_params[func]['response'].append( res['s:complexType']['s:sequence']['s:element']['@name'].strip() )
						if res['s:complexType']['s:sequence']['s:element']['@name'].strip().endswith('Result') and 'ArrayOf' in res['s:complexType']['s:sequence']['s:element']['@type']:
							self.func_params[func]['responseIsArray'] = True

	#############################################################################
	### Initializes function parameters
	#############################################################################
	def __initFunc(self):
		return 	{
			'response': [],
			'responseIsArray': False,
			'params': { 'required': [], 'optional': [] },
			'user': '',
			'pass': '',
			'entity': '',
		}

	#############################################################################
	### Generates WsSegPass
	#############################################################################
	def __generateWsSegPass(self) -> str:
		#1. Get UTC time
		now_utc = datetime.now(timezone.utc) # UTC current date and time
		datetimeUTC = now_utc.strftime("%Y%m%d%H%M%S").strip()

		#2. concat datetime and password
		datePwd = datetimeUTC + self.password.strip()

		#3. encode to UTF-8 and calculate hash SHA-256
		pwdHash = sha256( datePwd.encode().strip() ).digest()

		#4. encode to base64 and pass to string
		b64Str = base64.b64encode( pwdHash.strip() ).decode().strip()

		#5. concat dateTime and hash
		wsSegPass = datetimeUTC + b64Str

		return wsSegPass.strip()

	#############################################################################
	### Generates XML
	### api: API name
	### func: Function name
	### params: Parameters
	#############################################################################
	def getXML(self, api, func, params) -> str:
		return self._xml \
			.replace('$USERNAME$', self.username) \
			.replace('$WSSEGPASS$', self.__generateWsSegPass()) \
			.replace('$XMLNS$', self._url[api]['xmlns']) \
			.replace('$FUNCTION$', func) \
			.replace('$PARAMETERS$', params)

	#############################################################################
	### Calls API
	### api: API name
	### func: Function name
	### params: Parameters
	### mapParams: Map parameters
	#############################################################################
	def callAPI(self, api, func, params, mapParams = {}) -> dict[str, str]:
		if api not in self._url:
			return {'result': 'error', 'msg': 'API not found'}
		
		self.__setFuncParams(api)

		if func not in self.func_params or len(self.func_params[func]['params']['required']) > len(params):
			return {'result': 'error', 'msg': 'Function not found'}

		rParams = ''
		for param in params:
			if param in self.func_params[func]['params']['required'] or param in self.func_params[func]['params']['optional']:
				rParams += '<' + param + '>' + str(params[param]) + '</' + param + '>'
		
		xml = self.getXML(api = api, func = func, params = rParams) \
			.replace('$wsseg_user$', self.func_params[func]['user'] ) \
			.replace('$wsseg_pass$', self.func_params[func]['pass'] ) \
			.replace('$pk_entidad$', 
				('<' + self.func_params[func]['entity'] + '>' + 
					self.entity + 
					'</' + self.func_params[func]['entity'] + 
					'>') if self.func_params[func]['entity'] != '' else ''
			)
		
		response = requests.post(
			self._url[api]['api'].replace('$ENTITY$', self.entity).replace('$MODE$', 'pre-' if self.mode else ''), 
			data = xml, 
			headers = self._headers).text
		result = xmltodict.parse(response)['soap:Envelope']['soap:Body']

		for res in self.func_params[func]['response']:
			if res not in result:
				return {'result': 'error', 'msg': 'Function not found'}
			result = result[res]
		if result is None or len(result) == 0:
			return {'result': 'ok', 'data': {}}
		
		if len(mapParams) > 0:
			if not self.func_params[func]['responseIsArray']:
				retValues = {'result': 'ok', 'msg': 'ok', 'data': mapParams}
				for field, resField in retValues['data'].items():
					try:
						retValues['data'][field] = result[resField] if str(result[resField]) is not "{'@xsi:nil': 'true'}" else None
					except:
						pass
			else:
				retValues = {'result': 'ok', 'msg': 'ok', 'data': []}
				for res in result:
					retData = mapParams.copy()
					for field, resField in retData.items():
						try:
							retData[field] = res[resField] if str(res[resField]) is not "{'@xsi:nil': 'true'}" else None
						except:
							pass
					retValues['data'].append(retData)

		else:
			retValues = {'result': 'ok', 'msg': 'ok', 'data': result}

		return retValues
