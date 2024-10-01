import os


def build_structure(
    root_dir,
    structure=None,
    relative_path="",
):
    if structure is None:
        structure = {}

    for item in os.listdir(root_dir):
        item_path = os.path.join(
            root_dir, item,
        )
        item_relative_path = (
            os.path.join(
                relative_path, item,
            )
        )
        if os.path.isdir(item_path):
            if item not in structure:
                structure[item] = {}
            build_structure(
                item_path,
                structure[item],
                item_relative_path,
            )
        elif os.path.isfile(item_path):
            key = item.replace(
                ".csv", "",
            ).replace(".cypher", "")
            if key not in structure:
                structure[key] = {}
            if item.endswith(".csv"):
                structure[key][
                    "data"
                ] = item_relative_path
                print(
                    f"Added CSV path: {item_relative_path} to key: {key}",
                )
            elif item.endswith(
                ".cypher",
            ):
                structure[key][
                    "cypher"
                ] = item_relative_path
                print(
                    f"Added Cypher path: {item_relative_path} to key: {key}",
                )
    return structure


def merge_structures(
    load_files_structure,
    queries_structure,
):
    merged_structure = {}

    def merge_recursive(
        load_dict, query_dict,
    ):
        merged = {}
        for key in load_dict:
            merged[key] = {}
            if key in query_dict:
                if isinstance(
                    load_dict[key], dict,
                ) and isinstance(
                    query_dict[key],
                    dict,
                ):
                    merged[key] = (
                        merge_recursive(
                            load_dict[
                                key
                            ],
                            query_dict[
                                key
                            ],
                        )
                    )
                else:
                    merged[key] = {
                        "data": load_dict[
                            key
                        ].get(
                            "data", None,
                        ),
                        "cypher": query_dict[
                            key
                        ].get(
                            "cypher",
                            None,
                        ),
                    }
            else:
                merged[key] = load_dict[
                    key
                ]
        for key in query_dict:
            if key not in merged:
                merged[key] = (
                    query_dict[key]
                )
        return merged

    merged_structure = merge_recursive(
        load_files_structure,
        queries_structure,
    )
    return merged_structure


def generate_load_dataset_from_folder(
    parent_folder,
):

    load_files_dir = os.path.join(
        parent_folder, "load_files",
    )
    queries_dir = os.path.join(
        parent_folder, "queries",
    )

    print(
        "Building structure for load_files...",
    )
    load_files_structure = (
        build_structure(load_files_dir)
    )
    print(
        "Load files structure:",
        load_files_structure,
    )

    print(
        "Building structure for queries...",
    )
    queries_structure = build_structure(
        queries_dir,
    )
    print(
        "Queries structure:",
        queries_structure,
    )

    print("Merging structures...")
    merged_structure = merge_structures(
        load_files_structure,
        queries_structure,
    )
    print(
        "Merged structure:",
        merged_structure,
    )

    return merged_structure
