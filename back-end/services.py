from sklearn.datasets import load_iris

def get_data_set(iris):
    data = iris.data.tolist()
    target = iris.target.tolist()
    target_names = iris.target_names.tolist()
    data = [
        {
            "sepal_length": item[0],
            "sepal_width": item[1],
            "petal_length": item[2],
            "petal_width": item[3],
            "target": target[i],
            "target_name": target_names[target[i]]
        } for i, item in enumerate(data)
    ]

    return data