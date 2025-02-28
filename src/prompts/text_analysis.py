import json

from src.prompts import Prompt

# analyze_text_prompt = """
#     You are an audio transcription editor specialized in Portuguese language content. I'll provide you with a full transcription and its segments from a recorded speech in Portuguese.
#
#     Your task:
#     1. Read the full transcription to understand the context
#     2. Analyze each segment and decide whether to keep or remove it based on the transcription
#     3. Remove segments that:
#        - Don't make logical sense
#        - Contain repetitions or duplications of content
#        - Contain obvious mistakes, stutters, or filler words (like "hum", "tipo", "então", "enfim")
#        - Contain unfinished thoughts or sentences
#     4. Return only the segments that should be kept and does not contain repetitions or duplications of content
#
#     Pay special attention to Portuguese-specific speech patterns and filler words.
#
#     Example of input data:
#     [
#         "start": 42.658, "end": 45.278, "text": "O que você vai fazer? Você vai vir aqui no LinkedIn...",
#         "start": 51.81, "end": 54.43, "text": "Você vai vir aqui no LinkedIn, vai pesquisar aqui, ó.",
#         "start": 54.69, "end": 55.742, "text": "Dessa forma aqui, ó.",
#         "start": 61.186, "end": 63.102, "text": "O que você vai fazer? Você vai vir aqui no LinkedIn",
#         "start": 63.522, "end": 65.118, "text": "vai pesquisar assim dessa forma.",
#     ]
#
#     Example of output expected for this input:
#     [
#         "start": 61.186, "end": 63.102, "text": "O que você vai fazer? Você vai vir aqui no LinkedIn",
#         "start": 63.522, "end": 65.118, "text": "vai pesquisar assim dessa forma."
#     ]
#
#     Another example of input data:
#     [
#         "start": 40.066, "end": 42.494, "text": "Não funciona, não funciona."
#         "start": 42.658, "end": 45.278, "text": "O que você vai fazer? Você vai vir aqui no LinkedIn..."
#         "start": 47.458, "end": 48.318, "text": "Posição."
#         "start": 61.186, "end": 63.102, "text": "O que você vai fazer? Você vai vir aqui no LinkedIn"
#         "start": 63.522, "end": 65.118, "text": "vai pesquisar assim dessa forma."
#     ]
#
#     And the expected output for this input:
#
#     [
#         "start": 40.066, "end": 42.494, "text": "Não funciona, não funciona."
#         "start": 61.186, "end": 63.102, "text": "O que você vai fazer? Você vai vir aqui no LinkedIn"
#         "start": 63.522, "end": 65.118, "text": "vai pesquisar assim dessa forma."
#     ]
#
#     When I mean I need to keep the context and make sure the logic is correct, this is one example:
#
#     This is the input data:
#     [
#         'start': 8.066, 'end': 10.014, 'text': 'Se você está procurando vaga no LinkedIn,'
#         'start': 10.274, 'end': 11.262, 'text': 'Dessa forma.'
#         'start': 11.458, 'end': 13.15, 'text': 'Você está fazendo muito errado.'
#     ]
#
#     The response should be exactly the same as the input data in this case:
#     [
#         'start': 8.066, 'end': 10.014, 'text': 'Se você está procurando vaga no LinkedIn,'
#         'start': 10.274, 'end': 11.262, 'text': 'Dessa forma.'
#         'start': 11.458, 'end': 13.15, 'text': 'Você está fazendo muito errado.'
#     ]
#
#     Because if I remove the second segment, the context will change and the logic will be incorrect. So, keep this in consideration when making the decision.
#
#     The response should be a valid JSON array of segment objects, each with:
#     - "start": the start time (in seconds)
#     - "end": the end time (in seconds)
#     - "text": the segment text (unchanged if kept)
#
#     Input data:
#     {input_data}
#
#     Output only valid JSON with no explanations.
# """


learning_cases = [
    {
        "input": {
            "segments": [
                {
                    "start": 8.066,
                    "end": 10.014,
                    "text": "Se você está procurando vaga no LinkedIn,"
                },
                {
                    "start": 10.274,
                    "end": 11.262,
                    "text": "Dessa forma."
                },
                {
                    "start": 11.458,
                    "end": 13.15,
                    "text": "Você está fazendo muito errado."
                },
                {
                    "start": 21.026,
                    "end": 21.79,
                    "text": "Primeira coisa..."
                },
                {
                    "start": 22.338,
                    "end": 25.758,
                    "text": "Primeira coisa aqui, não usa essa aba de jobs aqui. Isso aqui é"
                },
                {
                    "start": 25.89,
                    "end": 26.75,
                    "text": "Péssimo."
                }
            ],
            "captions": "Se você está procurando vaga no LinkedIn dessa forma, você está fazendo muito errado. Primeira coisa aqui, não use essa aba de jobs. Isso aqui é péssimo"
        },
        "expected_output": [
            {
                "start": 8.066,
                "end": 10.014,
                "text": "Se você está procurando vaga no LinkedIn,"
            },
            {
                "start": 10.274,
                "end": 11.262,
                "text": "Dessa forma."
            },
            {
                "start": 11.458,
                "end": 13.15,
                "text": "Você está fazendo muito errado."
            },
            {
                "start": 22.338,
                "end": 25.758,
                "text": "Primeira coisa aqui, não usa essa aba de jobs aqui. Isso aqui é"
            },
            {
                "start": 25.89,
                "end": 26.75,
                "text": "Péssimo."
            }
        ],
    },
    {
        "input": {
            "segments": [
                {
                    "start": 212.674,
                    "end": 218.398,
                    "text": "Então, por que isso funciona? Porque quando você vai postar uma vaga na aba de Jobs,"
                },
                {
                    "start": 218.53,
                    "end": 220.062,
                    "text": "Você paga muito caro pra isso."
                },
                {
                    "start": 220.226,
                    "end": 235.358,
                    "text": "E tem muito recrutador hoje que tem parceria com empresas, então eles ganham dinheiro por trazer pessoas para a empresa. Então eles geralmente compartilham para a própria rede deles. Então eles fazem um post que as pessoas mesmo vão interagindo e vão compartilhando aquilo lá para outras pessoas."
                },
                {
                    "start": 235.586,
                    "end": 239.006,
                    "text": "Dessa forma você consegue falar diretamente com o recrutador que está ali,"
                },
                {
                    "start": 240.418,
                    "end": 242.942,
                    "text": "Dessa forma você consegue falar diretamente com o recrutador."
                },
                {
                    "start": 243.362,
                    "end": 244.318,
                    "text": "Então você vai..."
                },
                {
                    "start": 244.45,
                    "end": 246.366,
                    "text": "Passar na frente de muita gente..."
                },
                {
                    "start": 248.61,
                    "end": 251.198,
                    "text": "Então você vai estar passando na frente de muita gente."
                },
                {
                    "start": 251.426,
                    "end": 252.478,
                    "text": "Se você gostou,"
                },
                {
                    "start": 254.242,
                    "end": 256.126,
                    "text": "Se você gostou, já me segue pra mais dicas."
                }
            ],
            "captions": "Então por isso funciona Porque quando você posta uma vaga na aba de Jobs Você paga muito caro pra isso E tem muito recrutador hoje que tem parceria com empresas então eles ganham dinheiro por trazer pessoas para a empresa Então eles geralmente compartilham para a própria rede deles Então eles fazem um post que as pessoas mesmo vão interagindo e vão compartilhando aquilo lá para outras pessoas Dessa forma você consegue falar diretamente com o recrutador Então você vai estar passando na frente de muita gente Se gostou já me segue pra mais dicas"
        },
        "expected_output": [
            {
                "start": 212.674,
                "end": 218.398,
                "text": "Então, por que isso funciona? Porque quando você vai postar uma vaga na aba de Jobs,"
            },
            {
                "start": 218.53,
                "end": 220.062,
                "text": "Você paga muito caro pra isso."
            },
            {
                "start": 220.226,
                "end": 235.358,
                "text": "E tem muito recrutador hoje que tem parceria com empresas, então eles ganham dinheiro por trazer pessoas para a empresa. Então eles geralmente compartilham para a própria rede deles. Então eles fazem um post que as pessoas mesmo vão interagindo e vão compartilhando aquilo lá para outras pessoas."
            },
            {
                "start": 240.418,
                "end": 242.942,
                "text": "Dessa forma você consegue falar diretamente com o recrutador."
            },
            {
                "start": 248.61,
                "end": 251.198,
                "text": "Então você vai estar passando na frente de muita gente."
            },
            {
                "start": 254.242,
                "end": 256.126,
                "text": "Se você gostou, já me segue pra mais dicas."
            }
        ],
    }
]


def generate_learning_cases_text():
    learning_cases_text = ""
    for i, case in enumerate(learning_cases):
        learning_cases_text += f"Case #{i + 1}\nInput:\n{{{json.dumps(case['input'], ensure_ascii=False)}}}\n\nExpected Output:\n{{{json.dumps(case['expected_output'], ensure_ascii=False)}}}\n\n"

    return learning_cases_text


def generate_select_segments_prompt(input_data):
    prompt = select_segments_based_on_captions_temp_prompt.user_prompt.format(
        input_data=json.dumps(input_data, ensure_ascii=False)
    )

    prompt += """
    ----------
    
    # Learning from past errors
    Here are a couple of cases where mistakes were made in previous outputs, so I am showing the expected output:
    """ + generate_learning_cases_text()

    return prompt


select_segments_based_on_captions_temp_prompt = Prompt(
    user_prompt="""
    You are an expert in editing and refining transcriptions for spoken Portuguese content. 
    I'll provide you speech segments from a recorded video in Portuguese in a JSON format and the correct caption of the same video in a text format.
            
    Your task:
    1. Compare the segments with the captions in a chronological order and adjust the segments to perfectly match the captions.
    2. Do not merge segments. Keep the segments as they are.
    3. Return the segments in the same order as they are in the input data
    4. If there are duplicated segments for the same caption part, keep only the last one.
    5. Return the segments in the same JSON structure as the input data
    
    Output only valid JSON with no explanations.
    
    Input data:
    {input_data}
    """,
    system_prompt="""
    You are an expert in refining Portuguese speech transcriptions while preserving full context.
    """,
)

select_segments_based_on_captions_prompt = Prompt(
    user_prompt="""
    You are an expert in editing and refining transcriptions for spoken Portuguese content. 
    I will provide you with speech segments from a recorded video in Portuguese in JSON format and the script of the same video as a text format.
    
    # Your Task
    1. Understand Context & Objective
    - Read the script carefully to understand the complete meaning and intent of the video.
    
    2. Filter Out Mistakes & Duplicates
    - Remove segments that does not is on the script, either because I did talk wrongly or mistaken or is duplicated.
    - If a sentence or phrase is repeated, keep only the last correct version, unless an earlier version is necessary to maintain logical flow.
    - Do NOT remove any segment or phrase that contributes to the overall meaning or smooth transition between ideas. If removing a segment changes the meaning or weakens the flow, it must be kept.
    
    3. Preserve Segment Order & Format
    - Maintain the original order of the segments while filtering.
    - Do not modify the segment words.
    - Do not merge segments.
    
    4. Output Format
    - Return the cleaned-up segments in a valid JSON array with the same structure:
        - "start": the segment’s start time (in seconds)
        - "end": the segment’s end time (in seconds)
        - "text": the segment text (unchanged if kept)
    
    # Important Rules for Filtering
    
    ## Preserve Context & Meaning
    - Every sentence in the final captions must be fully represented in your output.
    
    # Output Requirements
    - Output only valid JSON with no explanations, comments, or extra text.
    
    # Here is the input data
    ## Script:
    {captions}
    
    ## Speech Segments:
    {segments}
    
    ----------------
    
    # Learn from past errors
    Case #1
    ```
    Script in this case:
    Se você está procurando vaga no LinkedIn dessa forma, você está fazendo muito errado. Primeira coisa aqui, não usa essa aba de jobs aqui. Isso aqui é Péssimo. Olha todas as vagas, quantos aplicantes.
    
    Speech Segments text in this case:
    Se você está procurando vaga no LinkedIn, Dessa forma. Você está fazendo muito errado. Primeira coisa... Primeira coisa aqui, não usa essa aba de jobs aqui. Isso aqui é Péssimo. Olha todas as vagas, quantos aplicantes.
    
    Expected output text in this case:
    Se você está procurando vaga no LinkedIn dessa forma, você está fazendo muito errado. Primeira coisa aqui, não usa essa aba de jobs aqui. Isso aqui é Péssimo. Olha todas as vagas, quantos aplicantes.
    ```
    """,
    system_prompt="""
        You are a helpful assistant that outputs valid JSON.
        Your response must be a properly formatted JSON array of segments to keep.
    """
)

# select_segments_based_on_captions_prompt = """
#     You are an audio transcription editor specialized in Portuguese language content. 
#     I'll provide you with segments from a recorded speech in Portuguese in a JSON format and the final and refined version of the video captions in a text format.

#     Your task:
#     1. Compare the segments with the captions and remove the segments that are not present in the captions
#     2. Return the kept segments in the same order as they are in the input data
#     3. Return the segments in a valid JSON array of "segment" objects, each with:
#         - "start": the start time (in seconds)
#         - "end": the end time (in seconds)
#         - "text": the segment text (unchanged if kept)

#     Input data:
#     {input_data}

#     Output only valid JSON with no explanations.
# """
