def format_phone_result(result: dict) -> str:
    if not result.get("valid"):
        return "❌ Número inválido ou não reconhecido."

    return (
        "📞 Análise do Número\n\n"
        f"• Número: {result['formatted']}\n"
        f"• País: {result['country']}\n"
        f"• Região: {result['local_region']} ({result['macro_region']})"
    )
