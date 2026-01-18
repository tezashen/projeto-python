import phonenumbers
import pycountry
from phonenumbers import geocoder, NumberParseException
import pycountry_convert as pc

# Mapa de estados brasileiros → macrorregião
BR_REGIOES = {
    "Acre": "Norte",
    "Alagoas": "Nordeste",
    "Amapá": "Norte",
    "Amazonas": "Norte",
    "Bahia": "Nordeste",
    "Ceará": "Nordeste",
    "Distrito Federal": "Centro-Oeste",
    "Espírito Santo": "Sudeste",
    "Goiás": "Centro-Oeste",
    "Maranhão": "Nordeste",
    "Mato Grosso": "Centro-Oeste",
    "Mato Grosso do Sul": "Centro-Oeste",
    "Minas Gerais": "Sudeste",
    "Pará": "Norte",
    "Paraíba": "Nordeste",
    "Paraná": "Sul",
    "Pernambuco": "Nordeste",
    "Piauí": "Nordeste",
    "Rio de Janeiro": "Sudeste",
    "Rio Grande do Norte": "Nordeste",
    "Rio Grande do Sul": "Sul",
    "Rondônia": "Norte",
    "Roraima": "Norte",
    "Santa Catarina": "Sul",
    "São Paulo": "Sudeste",
    "Sergipe": "Nordeste",
    "Tocantins": "Norte"
}


def analyze_phone_number(phone: str) -> dict:
    """
    Analisa um número de telefone e retorna informações estruturadas.
    Pode ser usado em Telegram, WhatsApp, API, CLI, etc.
    """

    if not phone.startswith("+"):
        phone = "+55" + phone

    try:
        number = phonenumbers.parse(phone, None)

        if not phonenumbers.is_valid_number(number):
            return {
                "valid": False,
                "error": "Número inválido"
            }

        iso = phonenumbers.region_code_for_number(number)

        country_obj = pycountry.countries.get(alpha_2=iso)
        country = country_obj.name if country_obj else "Desconhecido"

        local_region = geocoder.description_for_number(number, "pt_BR")

        # Brasil → macrorregião
        if iso == "BR":
            macro_region = BR_REGIOES.get(local_region, "Região desconhecida")
        else:
            try:
                continent_code = pc.country_alpha2_to_continent_code(iso)
                macro_region = pc.convert_continent_code_to_continent_name(continent_code)
            except Exception:
                macro_region = "Região desconhecida"

        formatted = phonenumbers.format_number(
            number,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

        return {
            "valid": True,
            "input": phone,
            "formatted": formatted,
            "country": country,
            "country_code": iso,
            "local_region": local_region,
            "macro_region": macro_region
        }

    except NumberParseException:
        return {
            "valid": False,
            "error": "Não foi possível interpretar o número"
        }
