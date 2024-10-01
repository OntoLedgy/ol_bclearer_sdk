import pandas as pd
from neo4j import Driver


class Neo4jSession:
    def __init__(
        self,
        driver: Driver,
        database_name: str,
    ):
        self.session = driver.session(
            database=database_name,
        )

    def execute_cypher_query(
        self,
        query,
    ):
        with self.session as session:
            result = session.run(query)
            records = list(result)
            return records

    def execute_cypher_query_with_parameters(
        self,
        query,
        params={},
        output="all",
    ):
        if output not in [
            "all",
            "none",
            "summary",
        ]:
            print(
                "ERROR: output parameter must have one of the follwing values :'all','none','summary' ",
            )
            return

        bShowSummary = True
        bShowData = True
        if output != "all":
            bShowData = False

        if output == "none":
            bShowSummary = False

        qq = query.strip()
        if len(qq) > 50:
            qq = (
                qq[0:76].replace(
                    "\n",
                    "",
                )
                + "..."
            )

        if bShowSummary:
            print(f"run_cypher : {qq}")

        with self._driver.session(
            database=self._dbname,
        ) as session:
            result = session.run(
                query.strip(),
                params,
            )

            df = pd.DataFrame(
                [
                    r.values()
                    for r in result
                ],
                columns=result.keys(),
            )

            results_summary = (
                result.consume()
            )

            if df.size > 0:
                if bShowSummary:
                    print(
                        "Results available after "
                        + str(
                            results_summary.result_available_after,
                        )
                        + "ms, finished query after "
                        + str(
                            results_summary.result_consumed_after,
                        )
                        + "ms",
                    )

        summary_counters = (
            results_summary.counters
        )

        df2 = pd.DataFrame(
            columns=[
                "counter",
                "value",
            ],
        )

        show = True

        if (
            summary_counters.nodes_created
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "nodes created",
                summary_counters.nodes_created,
            ]
        if (
            summary_counters.nodes_deleted
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "nodes deleted",
                summary_counters.nodes_deleted,
            ]
        if (
            summary_counters.relationships_created
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "relationships created",
                summary_counters.relationships_created,
            ]
        if (
            summary_counters.relationships_deleted
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "relationships deleted",
                summary_counters.relationships_deleted,
            ]
        if (
            summary_counters.properties_set
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "properties set",
                summary_counters.properties_set,
            ]
        if (
            summary_counters.labels_added
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "labels added",
                summary_counters.labels_added,
            ]
        if (
            summary_counters.labels_removed
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "labels removed",
                summary_counters.labels_removed,
            ]
        if (
            summary_counters.indexes_added
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "indexes added",
                summary_counters.indexes_added,
            ]
        if (
            summary_counters.indexes_removed
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "indexes removed",
                summary_counters.indexes_removed,
            ]
        if (
            summary_counters.constraints_added
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "constraints added",
                summary_counters.constraints_added,
            ]
        if (
            summary_counters.constraints_removed
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "constraints removed",
                summary_counters.constraints_removed,
            ]
        if (
            summary_counters.system_updates
            > 0
        ):
            df2.loc[len(df2.index)] = [
                "system updates",
                summary_counters.system_updates,
            ]
        if bShowData:
            if df.size > 0:
                print(df)
                show = False

        if bShowSummary:
            if df2.size > 0:
                print(df2)
                show = False

            if show:
                print(
                    "(no changes, no records)",
                )

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        self.session.close()
