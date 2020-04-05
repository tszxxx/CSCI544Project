## Segmentation part
Since Chinese word segmentations is different than the languages where each word is separated by a space, we suspect the accuracy and granularity of tokenization process can affect the results of any downstream task.
Therefore, we tried out four different tools and methods for tokenization.
- jieba package
- pkuseg package
- stanford core nlp package
- tokenize character by character

Explain code.

Example sentence:

末代皇帝溥仪(港)	溥仪（尊龙 饰）的一生在电影中娓娓道来。他从三岁起登基，年幼的眼光中只有大臣身上的一只蝈蝈，江山在他心中只是一个不明所以的名词。长大了，他以为可以变革，却被太监一把烧了朝廷账本。他以为是大清江山的主人，却做了日本人的傀儡。解放后，他坐上了从俄国回来的火车，身边是押送监视他的解放军。他猜测自己难逃一死，便躲在狭小的卫生间里，割脉自杀。然而他没有死在火车上，命运的嘲笑还在等着他。文革的风风雨雨，在他身上留下了斑斑伤痕。©豆瓣	尊龙,陈冲,邬君梅

Paths for segmented data:
- jieba package: jieba_data0/9.2-1293172.txt
- pkuseg package: pku_data0/9.2-1293172.txt
- stanford core nlp package: snlp_data0/9.2-1293172.txt
- character segmentation: char_data0/9.2-1293172.txt

