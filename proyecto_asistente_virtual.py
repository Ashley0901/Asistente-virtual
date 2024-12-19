import pyttsx3
import pyjokes
import webbrowser
import datetime
import pywhatkit
import wikipedia
import speech_recognition as sr


#opciones de voz/idioma
id1=r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id2=r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


#escuchar nuestro microfono y devolver el audio en texto
def transformar_audio_en_escritura():
    #almacenar recognizer en una variable
    r = sr.Recognizer()

    #configurar nuestro microfono
    with sr.Microphone() as origen:
        #tiempo de espera
        r.pause_threshold = 0.8

        #informar que empezo la grabacion
        print("ya puedes hablar:")

        #guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            #bucar en google
            pedido = r.recognize_google(audio, language= "es-mx")
            #prueba de que pudo ingresar
            print('Dijiste: ' + pedido)

            #devolver a pedido
            return pedido
        #en caso de que no comprenda el audio

        except sr.UnknownValueError:
            #prueba de que no comprendio el audio
            print('Ups no entendi')
            #devolver error

            return f'sigo esperando'

        #en caso de no resolver el pedido
        except sr.RequestError:
            #prueba de que no comprendio
            print("Uupppps no hay servicio")

            return f'sigo esperando'

        #error inesperado
        except:
            # prueba de que no comprendio
            print("Ups algo ha salido mal")
            return f'sigo esperando'

#hacer que nuestro asistente de voz hable
def hablar(mensaje):
    #inicializar el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice',id1)

    #darle el mensaje que va a decir
    engine.say(mensaje)

    #correr la voz y esperar a una nueva
    engine.runAndWait()

#metodo para pedir a nuestro asistente el dia de la semana
def pedir_dia():
    #guarda la fecha cumpleta del dia de hoy
    dia = datetime.date.today()
    #guarda el dia de la semana en el que nos encontremos
    dia_semana = dia.weekday()

    calendario = {0:'Lunes',
                  1:'Martes',
                  2:'Miercoles',
                  3:'Jueves',
                  4:'Viernes',
                  5:'Sábado',
                  6:'Domingo'}

    hablar(f'Hoy es el día {calendario[dia_semana]}')

#metodo para pedir la hora al asistente
def pedir_hora():
    hora = datetime.datetime.now()
    hora_actual = (f'En este momento son las {hora.hour} horas con {hora.minute} minutos'
                   f'y {hora.second} segundos')
    hablar(hora_actual)

def saludo_inicial():
    dia = datetime.datetime.now()
    hora = dia.hour
    if hora<6 or hora>20:
        momento = 'Buena noche'
    elif hora<=6 or hora<13:
        momento = 'Buen día'
    else:
        momento = 'Buena tarde'

    saludo = f'{momento}, Soy Sabina , tu asistente personal, en que te puedo ayudar?'
    hablar(saludo)

#metodo central en donde el asistente nos escucha y toma nuestra voz para realizar pedidos
def pedir_cosas():
    saludo_inicial()

    loop = True
    while loop:
        pedido = transformar_audio_en_escritura().lower()

        if 'abrir youtube' in pedido:
            hablar("Con gusto. Redirigiendo a youtube ")
            webbrowser.open('https://www.youtube.com/')
            continue

        elif 'abrir el navegador' in pedido:
            hablar('Claro que si. Redigiendo al navegador')
            webbrowser.open('https://www.google.com/')
            continue

        elif 'hora' in pedido:
            hablar(pedir_hora())
            continue

        elif 'día' in pedido:
            hablar(pedir_dia())
            continue

        elif 'busca en wikipedia' in pedido:
            hablar('Buscando en wikipedia.')
            pedido = pedido.replace('busca en wikipedia','')
            wikipedia.set_lang('es')
            busqueda = wikipedia.summary(pedido,sentences =1)
            hablar(f'Esto es lo que enconte en wikipedia: {busqueda}')
            continue

        elif 'busca en internet' in pedido:
            hablar('Como usted diga')
            pedido = pedido.replace('busca en internet','')
            pywhatkit.search(pedido)
            hablar(f"Esto es lo que he encontrado al buscar. {pedido}" )

        elif 'reproduce en youtube' in pedido:
            hablar('Que buena idea, reproduciendo en youtube')
            pedido = pedido.replace('reproduce en youtube','')
            pywhatkit.playonyt(pedido)
            continue

        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue

        elif 'adiós' in pedido:
            hablar('Fue un gusto ayudarte. Hasta pronto ')
            break

pedir_cosas()
