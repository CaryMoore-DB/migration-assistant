from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import CreateWarehouseRequestWarehouseType


class SqlWarehouseInfra():

    def __init__(self, config):

        self.config = config
        self.w = WorkspaceClient()
        self.default_sql_warehouse_name = "sql_migration_assistant_warehouse"


    def choose_compute(self):
        """
        User choose a warehouse which will be used for all migration assistant operations
        """
        warehouses = [f"CREATE A NEW SERVERLESS WAREHOUSE: {self.default_sql_warehouse_name}"]
        warehouses.extend(self.w.warehouses.list())

        print("Choose a warehouse: please enter the number of the warehouse you would like to use.\n"
              "This warehouse will be used for all migration assistant operations, setup and ongoing.")
        for i, warehouse in enumerate(warehouses):
            try:
                print(f"{i}: Name: {warehouse.name},\tType: {warehouse.warehouse_type.name},"
                      f"\tState: {warehouse.state.name},\tServerless: {warehouse.enable_serverless_compute}")
            except:
                print(f"{i}: {warehouse}")
        choice = int(input())
        if choice == 0:
            _ =self.w.warehouses.create_and_wait(
                name=self.default_sql_warehouse_name,
                cluster_size="2X-Small",
                max_num_clusters=1,
                enable_serverless_compute=True,
                enable_photon=True,
                warehouse_type=CreateWarehouseRequestWarehouseType.PRO,
                auto_stop_mins=10
            )
            warehouseID = _.id
        else:
            warehouseID = warehouses[choice].id
        # update config with user choice
        self.config['SQL_WAREHOUSE_ID'] = warehouseID
        self.config['SQL_WAREHOUSE_NAME'] = self.default_sql_warehouse_name

