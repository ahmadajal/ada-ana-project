import pandas as pd
import numpy as np
import scipy.stats as stats
import os 

def day_preprocess(day,data_day):
    data_single_day = data_day.get_group(day)
    data_single_day_gp = data_single_day.groupby('canton')
    # p_values
    data_single_day_p_values = pd.DataFrame(columns = ['canton','sentiment_pv','main_pv'])
    for i,group in enumerate( data_single_day_gp.groups):
        data_c = data_single_day_gp.get_group(group)
        pv_sentiment = stats.ttest_ind(a = data_c.sentiment, b= data_single_day.sentiment, equal_var=False)[1]
        pv_main = (stats.ttest_ind(a = data_c.clean_main_polarity, b= data_single_day.clean_main_polarity, equal_var=False))[1]
        data_single_day_p_values.loc[i] = [group, pv_sentiment, pv_main]
    data_single_day_p_values = data_single_day_p_values.set_index('canton')
    # mean
    data_single_day_mean = pd.DataFrame(data_single_day_gp.mean()[['clean_main_polarity','sentiment']])
    data_single_day_mean.columns = ['main_mean','sentiment_mean']
    # std
    data_single_day_std = pd.DataFrame(data_single_day_gp.std()[['clean_main_polarity','sentiment']])
    data_single_day_std.columns = ['main_std','sentiment_std']
    # count
    data_single_day_count = pd.DataFrame(data_single_day_gp.count()['sentiment'])
    data_single_day_count.columns = ['count']
    # languages
    data_single_day_nb_lang = pd.DataFrame(data_single_day_gp.sum()[['en','de']])
    data_single_day_nb_lang.columns = ['nb_en','nb_de']
    # concatenation
    data_single_day = pd.concat([data_single_day_mean, data_single_day_std, data_single_day_p_values, data_single_day_count,data_single_day_nb_lang], axis = 1, join = 'inner')
    data_single_day = data_single_day.reset_index()
    return data_single_day

def sentiment_value(name):
        if name == 'NEUTRAL':
            val = 0
        elif name == 'POSITIVE':
            val = 1
        elif name == 'NEGATIVE':
            val = -1
        else :
            val = np.NaN
        return val


def main():
    # reading files
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name_e = os.path.join(dir_path,"../data/output_tweets/sentiment_scored_english_tweets.csv")
    print("Reading " + file_name_e + "\n");
    data_e = pd.read_csv(file_name_e)
    del data_e['Unnamed: 0']
    print("Data shape : ")
    print(data_e.shape)

    file_name_g = os.path.join(dir_path,"../data/output_tweets/sentiment_scored_german_tweets.csv")
    print("Reading " + file_name_g + "\n");
    data_g = pd.read_csv(file_name_g)
    del data_g['Unnamed: 0']
    print("Data shape : ")
    print(data_g.shape)
    
    data = pd.concat([data_e,data_g])
    print(data.shape)

    # reading locations
    
    print("Reading locations' mapping\n");
    loc_to_canton = pd.read_csv(os.path.join(dir_path,"..data/location_to_canton.csv"))
    del loc_to_canton['Unnamed: 0']
    loc_to_canton.columns = [['canton','source_location']]
    print(loc_to_canton.shape[0])

    print("Percentage of unrepresented cantons in the data :");
    not_represented_cantons = loc_to_canton[loc_to_canton.source_location.isnull()]
    print(not_represented_cantons.shape[0]/loc_to_canton.shape[0])
    
    # mapping
    
    data_new = pd.merge(data, loc_to_canton, on='source_location', how='left')

    not_mapped_data = data_new[(data_new.canton).isnull()]
    percentage_not_mapped = not_mapped_data.shape[0] / data_new.shape[0]
    print("Size of unmapped data : ")
    print(not_mapped_data.shape[0])
    print("Percentage of unmapped data : ")
    print(percentage_not_mapped)

    # drop unmapped data
    mapped_data = data_new.dropna(subset= ['canton'], how='all')
    # take only relevent features
    data_sent_canton = mapped_data[['canton','sentiment','clean_main_polarity','published','lang']]
    
    print("Final data size : ")
    print(data_sent_canton.shape[0])

    # change sentiment value to int   
    data_sent_canton['sentiment'] = [sentiment_value(a) for a in data_sent_canton['sentiment']]

    # split date into day  hour
    data_sent_canton['published'] = [a.split('T')[0] for a in data_sent_canton['published']]
    data_sent_canton=data_sent_canton.rename(columns = {'published':'day'})

    # add english and german columns
    data_sent_canton['en'] = pd.Series(1*(data_sent_canton['lang']=='en'))
    data_sent_canton['de'] = pd.Series(1*(data_sent_canton['lang']=='de'))
    data_sent_canton.head()

    print("Aggregated data vizualisation \n")
    data_sent_canton_gp = data_sent_canton.groupby('canton')
    # p_values
    data_sent_canton_p_values = pd.DataFrame(columns = ['canton','sentiment_pv','main_pv'])
    for i,group in enumerate( data_sent_canton_gp.groups):
        data_c = data_sent_canton_gp.get_group(group)
        pv_sentiment = stats.ttest_ind(a = data_c.sentiment, b= data_sent_canton.sentiment, equal_var=False)[1]
        pv_main = (stats.ttest_ind(a = data_c.clean_main_polarity, b= data_sent_canton.clean_main_polarity, equal_var=False))[1]
        data_sent_canton_p_values.loc[i] = [group, pv_sentiment, pv_main]

    data_sent_canton_p_values = data_sent_canton_p_values.set_index('canton')
    # mean
    data_sent_canton_mean = pd.DataFrame(data_sent_canton_gp.mean()[['clean_main_polarity','sentiment']])
    data_sent_canton_mean.columns = ['main_mean','sentiment_mean']
    # std
    data_sent_canton_std = pd.DataFrame(data_sent_canton_gp.std()[['clean_main_polarity','sentiment']])
    data_sent_canton_std.columns = ['main_std','sentiment_std']
    # count
    data_sent_canton_count = pd.DataFrame(data_sent_canton_gp.count()['sentiment'])
    data_sent_canton_count.columns = ['count']
    # languages
    data_sent_canton_nb_lang = pd.DataFrame(data_sent_canton_gp.sum()[['en','de']])
    data_sent_canton_nb_lang.columns = ['nb_en','nb_de']

    # concatenation
    data_sent_canton_ = pd.concat([data_sent_canton_mean, data_sent_canton_std, data_sent_canton_p_values, data_sent_canton_count, data_sent_canton_nb_lang], axis = 1, join = 'inner')
    data_sent_canton_ = data_sent_canton_.reset_index()
    data_sent_canton_.to_json(os.path.join(dir_path,"../viz-data/__harvest3r_twitter_data-04_0.json"))
    
    print("Single day vizualisation \n")

    data_day = data_sent_canton.groupby(['day'])
    prefix= os.path.join(dir_path,"../viz-data/__harvest3r_twitter_data_")
    postfix = "-04_0.json"
    all_data_april = []

    for i in np.arange(30):
        if (i<9):
            day = '2016-04-0' + str(i+1)
        else : 
            day = '2016-04-' + str(i+1)
        print("Pre-processing " + day + "\n");
        data_sd = day_preprocess(day,data_day)
        data_sd.to_json(prefix + day.split('-')[2] + postfix)
        
if __name__ == '__main__':
    main()

