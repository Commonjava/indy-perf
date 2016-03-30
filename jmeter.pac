function FindProxyForURL(url, host){
	var DIRECT="DIRECT";
	var PROXY="PROXY jmeter.local:8888";

	if (dnsResolve(host) == "127.0.0.1" && url.contains('8080')) {
      return PROXY;
	}

	return DIRECT;
}