import re
import time
import difflib
import threading

import livecaption_translator as lc_trans


interface = lc_trans.Interface()


# 在子线程中进行翻译过程
def translate_thread(interface):
    ocr = lc_trans.Ocr(pos='实时辅助字幕')
    translator = lc_trans.Trans()

    def remove_overlap(new_text, full_text):
        # 在匹配之前，删除字符串中的换行符
        full_text_no_newlines = full_text.replace('\n', ' ')
        new_text_no_newlines = new_text.replace('\n', ' ')

        s = difflib.SequenceMatcher(None, full_text_no_newlines, new_text_no_newlines)
        match = s.find_longest_match(0, len(full_text_no_newlines), 0, len(new_text_no_newlines))

        # 去除重复的部分，只保留新文本中不同的部分
        new_unique_text = new_text_no_newlines[match.size:]

        return new_unique_text

    # 实现一个函数来分离并翻译完整句子
    def translate_complete_sentences(text):
        # 查找所有的完整句子，即以句号、问号或感叹号结尾的部分
        sentence_pattern = r'[^.!?\n]+[.!?]'
        sentences = re.findall(sentence_pattern, text)

        with open('translated_text.txt', 'a', encoding='utf-8') as file:
            for sentence in sentences:
                translated_sentence = translator.translate(sentence)
                # print(f'原文句子: {sentence}')
                # print(f'翻译结果:  {translated_sentence}')

                # 将翻译结果发送到GUI线程
                lc_trans.update_text(interface, sentence, translated_sentence)

                # 将原文句子和翻译结果写入到同一个文件，一行原文接着一行翻译
                file.write(f'原文: {sentence}\n')
                file.write(f'翻译: {translated_sentence}\n\n')

        # 移除已翻译的句子
        return re.sub(sentence_pattern, '', text)

    translate_interval = 2
    last_translation_time = time.time()

    full_text = ""
    last_text = ""

    running = True
    while running:
        current_time = time.time()

        text = ocr.get_text()
        new_text = remove_overlap(text, last_text)
        last_text = text

        if new_text:
            full_text += new_text
            # print("当前句子:", full_text)

        # 每隔三秒翻译一次
        if current_time - last_translation_time >= translate_interval:
            full_text = translate_complete_sentences(full_text)
            last_translation_time = current_time

            # 暂停1秒钟
        time.sleep(1)


translate_thread = threading.Thread(target=translate_thread, args=(interface,))
translate_thread.setDaemon(True)
translate_thread.start()


interface.run()
