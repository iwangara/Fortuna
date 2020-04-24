import utils
import configs
sql= utils.DBHelper()

dist =utils.Ranks().get_data()
print(dist)