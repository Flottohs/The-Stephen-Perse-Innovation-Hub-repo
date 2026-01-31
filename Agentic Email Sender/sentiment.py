from transformers import pipeline

clf = pipeline("text-classification",
               model="SamLowe/roberta-base-go_emotions",
               top_k=5)

text = input("Enter a sentence: ")
raw = clf(text)[0]

for result in raw:
    print(f"{result['label']:<12} || {result['score']:.4f}")
