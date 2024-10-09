from transformers import pipeline

# 加载预训练的情感分析模型
sentiment_analysis = pipeline("sentiment-analysis")

# 输入文本进行情感分析
texts = [
    "I love the new design of the website! It's so user-friendly.",
    "The service was terrible and the food was not good at all.",
    "It's okay, but I think it could be better."
]

# 对每个文本进行情感分析
results = sentiment_analysis(texts)

# 打印分析结果
for text, result in zip(texts, results):
    print(f"Text: {text}")
    print(f"Sentiment: {result['label']}, Confidence Score: {result['score']:.4f}\n")
