import json

from src.prompts import Prompt

learning_cases = [
    {
        "input": {
            "segments": [
                {
                    "start": 8.066,
                    "end": 10.014,
                    "text": "Se você está procurando vaga no LinkedIn,",
                },
                {"start": 10.274, "end": 11.262, "text": "Dessa forma."},
                {
                    "start": 11.458,
                    "end": 13.15,
                    "text": "Você está fazendo muito errado.",
                },
                {"start": 21.026, "end": 21.79, "text": "Primeira coisa..."},
                {
                    "start": 22.338,
                    "end": 25.758,
                    "text": "Primeira coisa aqui, não usa essa aba de jobs "
                    "aqui. Isso aqui é",
                },
                {"start": 25.89, "end": 26.75, "text": "Péssimo."},
            ],
            "captions": "Se você está procurando vaga no LinkedIn dessa forma,"
            " você está fazendo muito errado. Primeira coisa aqui,"
            " não use essa aba de jobs. Isso aqui é péssimo",
        },
        "expected_output": [
            {
                "start": 8.066,
                "end": 10.014,
                "text": "Se você está procurando vaga no LinkedIn,",
            },
            {"start": 10.274, "end": 11.262, "text": "Dessa forma."},
            {
                "start": 11.458,
                "end": 13.15,
                "text": "Você está fazendo muito errado.",
            },
            {
                "start": 22.338,
                "end": 25.758,
                "text": "Primeira coisa aqui, não usa essa aba de jobs aqui."
                " Isso aqui é",
            },
            {"start": 25.89, "end": 26.75, "text": "Péssimo."},
        ],
    },
    {
        "input": {
            "segments": [
                {
                    "start": 212.674,
                    "end": 218.398,
                    "text": "Então, por que isso funciona? Porque quando você"
                    " vai postar uma vaga na aba de Jobs,",
                },
                {
                    "start": 218.53,
                    "end": 220.062,
                    "text": "Você paga muito caro pra isso.",
                },
                {
                    "start": 220.226,
                    "end": 235.358,
                    "text": "E tem muito recrutador hoje que tem parceria com"
                    " empresas, então eles ganham dinheiro por trazer"
                    " pessoas para a empresa. Então eles geralmente"
                    " compartilham para a própria rede deles. Então"
                    " eles fazem um post que as pessoas mesmo vão"
                    " interagindo e vão compartilhando aquilo lá "
                    "para outras pessoas.",
                },
                {
                    "start": 235.586,
                    "end": 239.006,
                    "text": "Dessa forma você consegue falar diretamente com"
                    " o recrutador que está ali,",
                },
                {
                    "start": 240.418,
                    "end": 242.942,
                    "text": "Dessa forma você consegue falar diretamente com"
                    " o recrutador.",
                },
                {
                    "start": 243.362,
                    "end": 244.318,
                    "text": "Então você vai...",
                },
                {
                    "start": 244.45,
                    "end": 246.366,
                    "text": "Passar na frente de muita gente...",
                },
                {
                    "start": 248.61,
                    "end": 251.198,
                    "text": "Então você vai estar passando na frente de "
                    "muita gente.",
                },
                {"start": 251.426, "end": 252.478, "text": "Se você gostou,"},
                {
                    "start": 254.242,
                    "end": 256.126,
                    "text": "Se você gostou, já me segue pra mais dicas.",
                },
            ],
            "captions": "Então por isso funciona Porque quando você posta uma"
            " vaga na aba de Jobs Você paga muito caro pra isso"
            " E tem muito recrutador hoje que tem parceria com"
            " empresas então eles ganham dinheiro por trazer"
            " pessoas para a empresa Então eles geralmente"
            " compartilham para a própria rede deles Então eles"
            " fazem um post que as pessoas mesmo vão interagindo "
            "e vão compartilhando aquilo lá para outras pessoas"
            " Dessa forma você consegue falar diretamente com o"
            " recrutador Então você vai estar passando na frente"
            " de muita gente Se gostou já me segue pra mais dicas",
        },
        "expected_output": [
            {
                "start": 212.674,
                "end": 218.398,
                "text": "Então, por que isso funciona? Porque quando você vai"
                " postar uma vaga na aba de Jobs,",
            },
            {
                "start": 218.53,
                "end": 220.062,
                "text": "Você paga muito caro pra isso.",
            },
            {
                "start": 220.226,
                "end": 235.358,
                "text": "E tem muito recrutador hoje que tem parceria com"
                " empresas, então eles ganham dinheiro por trazer"
                " pessoas para a empresa. Então eles geralmente"
                " compartilham para a própria rede deles. Então"
                " eles fazem um post que as pessoas mesmo vão "
                "interagindo e vão compartilhando aquilo lá para "
                "outras pessoas.",
            },
            {
                "start": 240.418,
                "end": 242.942,
                "text": "Dessa forma você consegue falar diretamente com o"
                " recrutador.",
            },
            {
                "start": 248.61,
                "end": 251.198,
                "text": "Então você vai estar passando na frente de muita"
                " gente.",
            },
            {
                "start": 254.242,
                "end": 256.126,
                "text": "Se você gostou, já me segue pra mais dicas.",
            },
        ],
    },
]


def generate_learning_cases_text():
    learning_cases_text = ""
    for i, case in enumerate(learning_cases):
        learning_cases_text += (
            f"Case #{i + 1}\n"
            f"Input:\n{{{json.dumps(case['input'], ensure_ascii=False)}}}\n\n"
            f"Expected Output:\n"
            f"{{{json.dumps(case['expected_output'], ensure_ascii=False)}}}\n"
        )

    return learning_cases_text


def generate_select_segments_prompt(input_data):
    prompt = select_segments_based_on_captions_prompt.user_prompt.format(
        input_data=json.dumps(input_data, ensure_ascii=False)
    )

    prompt += (
        """
        ----------
        # Learning from past errors
        Here are a couple of cases where mistakes were made in previous
        outputs, so I am showing the expected output:
        """
        + generate_learning_cases_text()
    )

    return prompt


select_segments_based_on_captions_prompt = Prompt(
    user_prompt="""
    You are an expert in editing and refining transcriptions for spoken
    Portuguese content.
    I'll provide you speech segments from a recorded video in Portuguese in
    a JSON format and the correct caption of the same video in a text format.

    Your task:
    1. Compare the segments with the captions in a chronological order and
    adjust the segments to perfectly match the captions.
    2. Do not merge segments. Keep the segments as they are.
    3. Return the segments in the same order as they are in the input data
    4. If there are duplicated segments for the same caption part, keep only
     the last one.
    5. Return the segments in the same JSON structure as the input data

    Output only valid JSON with no explanations.

    Input data:
    {input_data}
    """,
    system_prompt="""
    You are an expert in refining Portuguese speech transcriptions while
    preserving full context.
    """,
)
