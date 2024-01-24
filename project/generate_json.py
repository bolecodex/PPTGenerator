import openai
import json

# optional; defaults to `os.environ['OPENAI_API_KEY']`
openai.api_key = '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'
def generate_json(word_content="", prompt="Generate a PPT of 5 slides", slideDeck={"slide_number": float(5), "title": "", "content": "", "narration": ""}):
    messages = [
            {"role": "system", "content": "User will ask you to create or update text content for some slides"+(" based on the aforementioned Input Article" if word_content else "")+". The response format should be a valid json format structured as this: [{\"slide_number\": <Float>, \"title\": \"<String>\", \"content\": \"<String>\", \"narration\": \"<String>\"},{\"slide_number\": <Float>, \"title\": \"<String>\", \"content\": \"<String>\", \"narration\": \"<String>\"}] \n content field in the response comprehensive enough as it is the main text of each slide. \n For content use a mix of bullet points and text when applicable. \n If you are modifying an existing slide leave the slide number unchanged but if you are adding slides to the existing slides, use decimal digits for the slide number. for example to add a slide after slide 2, use slide number 2.1, 2.2, ... \n If user asks to remove a slide, set its slide number to negative of its current value because slides with negative slide number will be excluded from presentation. \n The existing slides are as follows: "+json.dumps(slideDeck)},
            {"role": "system", "content": "For each slide the content field is the main body of the slide while the narration field is just an example transcript of the presentation of the content field. \n Never mention the slide number in the transcript."},
            {"role": "system", "content": "For each slide, the content field should be the default field to modify if modification is demanded by the user for the slide, not the narration field. "},
            {"role": "system", "content": "For each slide, the narration field should only be populated if explicitely asked in user prompt, otherwise should be left empty. "},
            {"role": "system", "content": "Response should be valid json in the format described earlier. slide_number, title,and content are mandatory keys."},
            # {"role": "system", "content": "The generated text content should keep the orginal language"},
            {"role": "user", "content": prompt}
        ]
    if word_content:
        messages.insert(0, {
            "role": "system",
            "content": "Input Article: " + word_content
            })
    print(messages)
    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    # 
    slides_data = json.loads(completion.choices[0].message.content)
    return slides_data
# word_content='最高法院法官伊贾祖尔·阿赫桑（Justice Ijazul Ahsan）在法官马扎哈尔·阿里·阿克巴·纳克维（Justice Mazahar Ali Akbar Naqvi）辞职一天后，于周四辞去了他的职位，这一消息令人震惊。阿赫桑法官原计划在法官卡齐·法伊兹·伊萨（CJP Qazi Faez Isa）之后成为巴基斯坦的下一任首席法官。根据致总统的辞职信，阿赫桑法官表示：“我不再希 望继续担任巴基斯坦最高法院法官。”他表示根据宪法第206（1）条的规定，他立即生效辞职。辞职信没有提及辞职的原因。总统阿里夫·阿尔维（Dr Arif Alvi）今天早些时候 接受了纳克维法官的辞职，纳克维法官面临着不当行为的投诉。纳克维法官一天前辞去了最高法院法官的职位。纳克维法官面临着最高司法委员会（SJC）对其不当行为的调查，去年10月发出了违纪通知。周二，最高法院拒绝了他要求暂停诉讼程序的请求。阿赫桑法官是五人委员会的一员，他于2023年11月22日拒绝与委员会的其他成员一起向纳克维法 官发出新的违纪通知。在周二致最高司法委员会成员的信中，阿赫桑法官对诉讼程序的匆忙表示遗憾，并表示在进行中的委员会程序中没有进行辩论和讨论。阿赫桑法官解释说 ，这种诉讼程序方式对整个过程产生了不必要的怀疑，因此他不同意所遵循的程序和进行诉讼程序的方式。信中提到了对法官的投诉中的指控，信中表示这些指控在法律上和事 实初步评估上都是毫无根据的。信中遗憾地指出，应该采取一种理性和审慎的方法，这将防止委员会陷入发出违纪通知的错误。阿赫桑法官是2017年高调的巴拿马门案五人小组 的一员，该案导致当时的总理纳瓦兹·谢里夫被取消资格。他还被任命为监督和监督巴拿马门案判决执行的监察法官。阿赫桑法官于2015年11月6日担任拉合尔高等法院首席法官 ，一年后的2016年6月28日晋升为最高法院法官。2023年4月10日，律师萨尔达尔·萨尔曼·艾哈迈德·多加尔（Sardar Salman Ahmad Dogar）向最高司法委员会提出了针对阿赫桑 法官和其他人的参考案。投诉指控前首席法官乌马尔·阿塔·班迪尔（Umar Ata Bandial）、阿赫桑法官和其他最高法院法官在2009年9月2日最高司法委员会发布的上级司法机构 法官行为准则中违反了行为准则。2023年4月14日，律师米安·道伍德（Mian Dawood）在最高司法委员会对八名最高法院法官提出了投诉，这些法官正在审理挑战削减首席法官权力的法案的请愿书。投诉书要求撤销前首席法官班迪尔、阿赫桑法官和其他人，理由是他们涉嫌不当行为和偏离法官行为准则。上个月，国防部的一名前高级官员向最高司法委 员会投诉阿赫桑法官和穆尼布·阿赫塔尔法官，称其违反了行为准则。巴基斯坦穆斯林联盟（PML-N）要求对阿赫桑法官和纳克维法官进行“问责”。PML-N信息秘书马里尤姆·奥兰 格泽布（Marriyum Aurangzeb）在拉合尔的新闻发布会上对辞职表示评论，并质疑为什么阿赫桑法官和纳克维法官选择辞职。“他们是否认为辞去最高法院法官的职位就可以摆脱他们所犯下的不公正行为？”奥兰格泽布指责这两名法官“对该国人民犯下了不公正行为”。她说：“作为联合调查组的监察法官，伊贾祖尔·阿赫桑法官似乎认为辞职可以抹去对该国六年来所犯下的不公正行为。”她强调，仅仅辞职并不能结束这件事，必须进行问责。奥兰格泽布指出，如果一个当选的总理都可以接受审查，那么任何个人，包括最高法院法官，都应该接受问责。“将最高法院变成一个嘲笑对象，并诋毁一个现在正获得提升地位的前总理是不可接受的，”她补充道。她进一步表示，那些“参与阴谋的人现在正在面临后果”。她说：“这是对每个人的警告，他们今天所做决定的真相将在未来揭示出来。滥用权力必然会在像阿赫桑法官和纳克维法官这样的个人命运'
# prompt="Generate a PPT of 3 slides"
# slides_data=generate_json(prompt=prompt, word_content=word_content)
# print(slides_data)
# new_prompt="Generate a PPT of 7 slides"
# slides_data=generate_json(prompt=new_prompt, word_content=word_content, slideDeck=slides_data)
# print(slides_data)