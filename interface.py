import gradio as gr
import re
from initial_i import find_initial_i_errors, EXCEPTIONS 

def correct_initial_i(text):
    corrected_text = ""
    last_index = 0
    pattern = r"\b([Ии])([А-Яа-яіїєґ'’\d-]*)" 
    
    for match in re.finditer(pattern, text):
        initial_letter = match.group(1) 
        rest_of_word = match.group(2)
        word = match.group(0) 
        start, end = match.start(), match.end()
        
        corrected_text += text[last_index:start]
        
        if word.lower() in EXCEPTIONS:
            corrected_text += word
        else:
            if initial_letter == 'И':
                corrected_text += 'І' + rest_of_word
            elif initial_letter == 'и':
                corrected_text += 'і' + rest_of_word
                
        last_index = end
        
    corrected_text += text[last_index:]
    return corrected_text


def process_text_and_correct(text: str):
    if not text:
        return [], "" 
        
    highlights = find_initial_i_errors(text)
    
    corrected_text = correct_initial_i(text)
    
    return highlights, corrected_text


HIGHLIGHT_COLOR_MAP = {
    "початкове-и": "red",
}

with gr.Blocks(theme="soft", css="""
#title {text-align:center; font-size: 32px; font-weight:700; margin-bottom:20px;}
""") as demo:

    gr.HTML("<div id='title'>Пошук порушень правила вживання 'і/и' на початку слова</div>")
    gr.Markdown(f"Винятки, що ігноруються: {', '.join(sorted(EXCEPTIONS))}")

    with gr.Row():
        with gr.Column(scale=6):
            text_input = gr.Textbox(
                label="Текст українською",
                info="Введіть текст для перевірки початкового 'і/и'",
                lines=10, 
                placeholder="Введіть текст...",
            )

            with gr.Row():
                clear_btn = gr.ClearButton()
                submit_btn = gr.Button("Перевірити та виправити", variant="primary") 

        with gr.Column(scale=6):
            result_highlight = gr.HighlightedText(
                label="Знайдені помилки",
                combine_adjacent=True,
                color_map=HIGHLIGHT_COLOR_MAP
            )
            
            result_corrected = gr.Textbox(
                label="Пропонований виправлений текст",
                lines=5,
                interactive=False
            )

    gr.Examples(
        examples=[
            "Истина криється у деталях. Икона старого письма.",
            "Иди сміливо вперед. Иноземець приніс иструмент.", 
            "Иноді ми бачимо иній вранці. Инший раз таке трапляється.",
            "На жаль, иноді ирій не настає, і идол стоїть на иржавій землі.",
            "Інститут історії. Іній покрив іскристу іскру.",
            "Ирод був злий. Инший день. Імовірність існує."
        ],
        inputs=text_input
    )

    submit_btn.click(
        process_text_and_correct, 
        inputs=text_input, 
        outputs=[result_highlight, result_corrected] 
    )
    
    clear_btn.click(lambda: ["", [], ""], None, [text_input, result_highlight, result_corrected])

demo.launch()