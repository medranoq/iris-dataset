def spices_graph(target: int):
    if target < 0 or target >= len(app.state.iris_data.target_names):
        return JSONResponse(
            status_code=404,
            content={"message": "Target not found"}
        )

    # Assuming you have a function to generate the graph
    graph_url = f"/static/{target}.jpg"

    return JSONResponse(
        content={
            "graph_url": graph_url,
            "target_name": app.state.iris_data.target_names[target]
        }
    )