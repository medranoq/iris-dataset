from sklearn.datasets import load_iris

def get_data_set():
    iris = load_iris()

    print(iris.keys())
    data = iris.data.tolist()
    target = iris.target.tolist()
    target_names = iris.target_names.tolist()

    for i in range(len(data)):
        data[i] = {
            "sepal_length": data[i][0],
            "sepal_width": data[i][1],
            "petal_length": data[i][2],
            "petal_width": data[i][3],
            "target": target[i],
            "target_name": target_names[target[i]]
        }

    return data