from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import random
import joblib
import os

# 라벨 정의
labels = {
    0: "개념 부족형",
    1: "준킬러 취약형",
    2: "킬러 취약형",
    3: "전략 부족형",
    4: "전반적 우수형"
}

# 컬럼 정의
columns = [f"Q{i+1}" for i in range(30)] + ["label"]

# 데이터 생성 함수
def generate_student_data(student_type):
    answers = []
    for i in range(30):
        if student_type == 0:  # 개념 부족형
            prob = 0.3 if i < 8 or (16 <= i < 22) else 0.6
        elif student_type == 1:  # 준킬러 취약형
            prob = 0.2 if i in [14, 19, 26] else 0.7
        elif student_type == 2:  # 킬러 취약형
            prob = 0.2 if i in [20, 21, 27, 28, 29] else 0.7
        elif student_type == 3:  # 전략 부족형
            prob = 0.1 if i in [20, 21, 27, 28, 29] else 0.9
        else:  # 전반적 우수형
            prob = 0.85
        answers.append(1 if random.random() < prob else 0)
    return answers

# 학습 데이터 100,000개 생성
data = []
for _ in range(100000):
    label = random.randint(0, 4)
    answers = generate_student_data(label)
    data.append(answers + [label])

df = pd.DataFrame(data, columns=columns)

# 학습/평가 분리
X = df.drop(columns=["label"])
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train/test 데이터 저장
train_df = X_train.copy()
train_df["label"] = y_train
test_df = X_test.copy()
test_df["label"] = y_test

os.makedirs("data", exist_ok=True)
train_df.to_csv("data/train.csv", index=False)
test_df.to_csv("data/test.csv", index=False)
print("train/test CSV 저장 완료!")

# 모델 학습
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# 평가 출력
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred, target_names=[labels[i] for i in range(5)]))

# 모델 저장
joblib.dump(clf, "model/student_type_classifier_100k.pkl")