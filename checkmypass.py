#Done by Asier Salvo (asiersalvo.com) follow @asiersalvo
#Just learning how to code in Python
#This was an exercise. Thanks!
import requests
import hashlib
import sys
#primero vamos a crear una función que checkea, recibe los 5 dígitos y checkea una llamada
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    # Esto password123 sería CBFDAC6008F9CAB4083784CBD1874F76618D2A97 pero se la vamos a pasar así: CBFDA
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Runtime fetching: {res.status_code}, check the API and try again.')
    return res

# def read_res(response):
#     print(response.text)
def get_password_leaks_count(hashes,hash_to_check):
    #creamos esta función que, tras la respuesta de la API, recibe las diferentes respuestas en hashes y luego
    #además la password nuestra que tiene que checkear en hash_to_check
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0
    #tener en cuenta en python SIEMPRE las posiciones, tabulaciones etc puesto que cambian el significado de las funciones.

#después vamos a generar otra función que nos checkee la función en sí
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail = sha1password[:5],sha1password[5:]
    response = request_api_data(first5_char)
    #print(first5_char,tail)
    #print(response)
    return get_password_leaks_count(response,tail)

#request_api_data('123')
def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} se ha hackeado {count} veces.')
        else:
            print('Tu contraseña está sana. Felicidades.')
    return 'Done!'

if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))