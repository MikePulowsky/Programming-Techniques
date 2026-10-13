from checker import build_url, is_https, show_response, check_site
    print(build_url("example.com", "/login"))
    print(build_url("example.com", "login"))
    
    print(is_https("example.com," "login"))
    print(is_https("ixample.com," "login"))
    
    show_response("https://example.com")
    
    check_site("https://example.com")
    check_site("http://this-site-does-not-exist.invalid")

