import numpy as np
import matplotlib.pyplot as plt
from ...services import get_data_set
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse,FileResponse

router = APIRouter(
    prefix="/graph",
    tags=["Graph"]
)

@router.get("/correlation")
async def correlation_graph(req: Request):
    iris_data = req.app.state.iris_data
    feature_names = iris_data.feature_names
    data = np.array(iris_data.data)

    # Calculate the correlation matrix
    correlation_matrix = np.corrcoef(data.T)

    # Create a heatmap
    plt.figure(figsize=(8, 6))
    plt.imshow(correlation_matrix, cmap="coolwarm", interpolation="nearest")
    plt.colorbar(label="Correlation Coefficient")
    plt.xticks(range(len(feature_names)), feature_names, rotation=45, ha="right")
    plt.yticks(range(len(feature_names)), feature_names)
    plt.title("Correlation Matrix of Iris Features")
    plt.tight_layout()

    # Save the plot to a file
    graph_path = "back-end/static/graph/correlation_matrix.jpg"
    plt.savefig(graph_path)
    plt.close()  # Close the plot to free memory

    # Return the image to be displayed in the browser
    return FileResponse(
        path=graph_path,
        media_type="image/jpeg"
    )


@router.get("/sepices/{target}")
async def iris_graph(req: Request, target: int):

    iris_data = req.app.state.iris_data
    target_names = iris_data.target_names.tolist()
    data = get_data_set(iris_data)

    if target < 0 or target >= len(target_names):
        return JSONResponse(
            status_code=404,
            content={"message": "Target not found"}
        )

    filtered_data = [item for item in data if item["target"] == target]

    if not filtered_data:
        return JSONResponse(
            status_code=404,
            content={"message": "No data found for the specified target"}
        )


    # Extract features for plotting

    features = np.array(
        [[item["sepal_length"], item["sepal_width"], item["petal_length"], item["petal_width"]] for item in
         filtered_data])

    target_name = target_names[target]
    # Create a scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(features[:, 0], features[:, 1], label=target_name, alpha=0.7)
    plt.title(f"Iris Species: {target_name.capitalize()}")
    plt.xlabel("Sepal Length")
    plt.ylabel("Sepal Width")
    plt.legend()
    plt.grid(True)
    # Save the plot to a file
    graph_path = f"back-end/static/graph/{target}.jpg"
    plt.savefig(graph_path)
    plt.close()  # Close the plot to free memory
    graph_url = f"/static/graph/{target}.jpg"

    # Return the image to be displayed in the browser
    return FileResponse(
        path=graph_path,
        media_type="image/jpeg"
    )


@router.get("/sepices/dist/{target}")
async def target_distribution(req: Request, target: int):
    iris_data = req.app.state.iris_data
    target_names = iris_data.target_names.tolist()
    data = get_data_set(iris_data)

    if target < 0 or target >= len(target_names):
        return JSONResponse(
            status_code=404,
            content={"message": "Target not found"}
        )

    # Filter data by target
    filtered_data = [item for item in data if item["target"] == target]

    if not filtered_data:
        return JSONResponse(
            status_code=404,
            content={"message": "No data found for the specified target"}
        )

    # Extract features for plotting
    features = np.array(
        [[item["sepal_length"], item["sepal_width"], item["petal_length"], item["petal_width"]] for item in filtered_data]
    )

    feature_names = ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"]

    # Create histograms for each feature
    plt.figure(figsize=(10, 8))
    for i, feature_name in enumerate(feature_names):
        plt.subplot(2, 2, i + 1)
        plt.hist(features[:, i], bins=10, color="skyblue", alpha=0.7)
        plt.title(f"Distribution of {feature_name}")
        plt.xlabel(feature_name)
        plt.ylabel("Frequency")
        plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()

    # Save the plot to a file
    graph_path = f"back-end/static/graph/distribution_{target}.jpg"
    plt.savefig(graph_path)
    plt.close()  # Close the plot to free memory

    # Return the image to be displayed in the browser
    return FileResponse(
        path=graph_path,
        media_type="image/jpeg"
    )
