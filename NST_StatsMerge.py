import pandas as pd

directory_in_str = "NaturalStatTrick_Data_Files"

dfBio = pd.read_csv(directory_in_str + "/" + "Bio-22-23.csv")
dfFiveOnFive = pd.read_csv(directory_in_str + "/" + "5-5-22-23.csv")
dfPK = pd.read_csv(directory_in_str + "/" + "PK-22-23.csv")
dfPP = pd.read_csv(directory_in_str + "/" + "PP-22-23.csv")
dfRelFiveOnFive = pd.read_csv(directory_in_str + "/" + "5-5-rel-22-23.csv")
dfRelPK = pd.read_csv(directory_in_str + "/" + "PK-rel-22-23.csv")
dfRelPP = pd.read_csv(directory_in_str + "/" + "PP-rel-22-23.csv")

print("All Data Files loaded")

dfBio.set_index(['Player', 'Team'], inplace=True)
dfFiveOnFive.set_index(['Player', 'Team'], inplace=True)
dfPK.set_index(['Player', 'Team'], inplace=True)
dfPP.set_index(['Player', 'Team'], inplace=True)
dfRelFiveOnFive.set_index(['Player', 'Team'], inplace=True)
dfRelPK.set_index(['Player', 'Team'], inplace=True)
dfRelPP.set_index(['Player', 'Team'], inplace=True)

print("indexes set")

# Create a dictionary of column mappings
column_mappings = {column: 'Bio_' + column if column != 'Player' else column for column in dfBio.columns}
# Rename columns using the dictionary
dfBio.rename(columns=column_mappings, inplace=True)

column_mappings = {column: '5-5_' + column if column != 'Player' else column for column in dfFiveOnFive.columns}
dfFiveOnFive.rename(columns=column_mappings, inplace=True)

column_mappings = {column: 'PK_' + column if column != 'Player' else column for column in dfPK.columns}
dfPK.rename(columns=column_mappings, inplace=True)

column_mappings = {column: 'PP_' + column if column != 'Player' else column for column in dfPP.columns}
dfPP.rename(columns=column_mappings, inplace=True)

column_mappings = {column: 'rel-5-5_' + column if column != 'Player' else column for column in dfRelFiveOnFive.columns}
dfRelFiveOnFive.rename(columns=column_mappings, inplace=True)

column_mappings = {column: 'rel-PK_' + column if column != 'Player' else column for column in dfRelPK.columns}
dfRelPK.rename(columns=column_mappings, inplace=True)

column_mappings = {column: 'rel-PP_' + column if column != 'Player' else column for column in dfRelPP.columns}
dfRelPP.rename(columns=column_mappings, inplace=True)

print("columns renamed")

#join all the dataframes together on player and team using an outer join.  I used 2 keys because there are 2 sebastian aho's and it screwed up all the outputs

dfMaster = pd.merge(dfBio, dfFiveOnFive, on=['Player', 'Team'], how='outer')
dfMaster = pd.merge(dfMaster, dfPK, on=['Player', 'Team'], how='outer')
dfMaster = pd.merge(dfMaster, dfPP, on=['Player', 'Team'], how='outer')
dfMaster = pd.merge(dfMaster, dfRelFiveOnFive, on=['Player', 'Team'], how='outer')
dfMaster = pd.merge(dfMaster, dfRelPK, on=['Player', 'Team'], how='outer')
dfMaster = pd.merge(dfMaster, dfRelPP, on=['Player', 'Team'], how='outer')

print("*************************")
print("dfMaster")
print(dfMaster.count)
# display
# dfBio.head()

print("Master data frame created")

dfMaster.to_csv(directory_in_str + "/" + "Output.csv")

print("output file created")
print("*************************")

