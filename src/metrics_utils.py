from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import seaborn as sns


def show_full_classification_report(true, prediction, class_labels=None):
    report = classification_report(true, prediction, output_dict=True)
    cm = confusion_matrix(true, prediction, normalize='true')

    class_keys = [k for k in report.keys() if k.isdigit() or isinstance(k, int)]
    class_keys = sorted(class_keys, key=lambda x: int(x))

    precision_vals = [report[k]['precision'] for k in class_keys]
    recall_vals = [report[k]['recall'] for k in class_keys]
    f1_vals = [report[k]['f1-score'] for k in class_keys]

    accuracy = report.get('accuracy', None)
    macro_avg = report.get('macro avg', {})
    weighted_avg = report.get('weighted avg', {})

    overall_metrics = [
        accuracy,
        macro_avg.get('precision', 0),
        macro_avg.get('recall', 0),
        macro_avg.get('f1-score', 0),
        weighted_avg.get('precision', 0),
        weighted_avg.get('recall', 0),
        weighted_avg.get('f1-score', 0)
    ]

    overall_labels = [
        'Accuracy',
        'Macro Prec.', 'Macro Rec.', 'Macro F1',
        'Weighted Prec.', 'Weighted Rec.', 'Weighted F1'
    ]

    fig = plt.figure(figsize=(22, 14))
    grid = plt.GridSpec(2, 4, height_ratios=[1, 2], hspace=0.4, wspace=0.5)

    ax1 = fig.add_subplot(grid[0, 0])
    ax1.bar(class_keys, precision_vals, color='skyblue')
    ax1.set_title('Precision by Class')
    ax1.set_ylim(0, 1.05)
    ax1.get_xlabel()
    ax1.set_xticks(class_keys)

    ax2 = fig.add_subplot(grid[0, 1])
    ax2.bar(class_keys, recall_vals, color='lightgreen')
    ax2.set_title('Recall by Class')
    ax2.set_ylim(0, 1.05)
    ax2.set_xticks(class_keys)

    ax3 = fig.add_subplot(grid[0, 2])
    ax3.bar(class_keys, f1_vals, color='salmon')
    ax3.set_title('F1-score by Class')
    ax3.set_ylim(0, 1.05)
    ax3.set_xticks(class_keys)

    fig.add_subplot(grid[0, 3]).axis('off')

    ax4 = fig.add_subplot(grid[1, 0:2])
    sns.heatmap(cm, annot=True, fmt='.2f', cmap='Blues',
                xticklabels=class_labels, yticklabels=class_labels, ax=ax4, square=True)
    ax4.set_title('Confusion Matrix (Normalized)', fontsize=14)
    ax4.set_xlabel('Predicted')
    ax4.set_ylabel('Actual')

    ax5 = fig.add_subplot(grid[1, 2:4])
    sns.barplot(x=overall_labels, y=overall_metrics, hue=overall_labels,
                palette='Set2', ax=ax5, legend=False)
    for i, v in enumerate(overall_metrics):
        ax5.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom', fontsize=9)
    ax5.set_ylim(0, 1.1)
    ax5.set_title('Overall Metrics', fontsize=14)
    ax5.set_ylabel('Score')
    ax5.tick_params(axis='x', labelrotation=30)
    plt.subplots_adjust(top=0.95, hspace=0.4, wspace=0.3)
    plt.show()


def print_report_dict(true, prediction):
    print(classification_report(true, prediction, output_dict=True))


def print_report_table(true, prediction):
    print(classification_report(true, prediction))



def print_token_importances(clf, X_test, Y_test, vectorizer, repeats=50, random=42):
    """
    Выводит важность токенов на основе permutation importance.

    Параметры:
    - clf: обученный классификатор
    - X_test: матрица признаков тестовой выборки (scipy matrix)
    - Y_test: целевые метки тестовой выборки
    - vectorizer: объект TfidfVectorizer, использованный для векторизации
    - repeats: количество повторов при permutation importance
    - random: random_state для воспроизводимости
    """
    result = permutation_importance(
        clf,
        X_test.toarray(),
        Y_test,
        n_repeats=repeats,
        random_state=random,
        scoring='f1_weighted'
    )

    feature_names = vectorizer.get_feature_names_out()
    importances = result.importances_mean

    tokens_with_scores = sorted(
        zip(feature_names, importances),
        key=lambda x: x[1],
        reverse=True
    )

    for token, score in tokens_with_scores:
        print(f"{token:10s} — {score:.6f}")


