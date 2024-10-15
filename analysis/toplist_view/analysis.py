import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TopListAnalysis:
    def __init__(self):
        self.target_lists_df = {}
        self.target_response = {}
        pass
    
    def load_data(self, input_dir):
        # load in GFW result
        in_GFW_dir = os.path.join(input_dir, "InGFW/")
        for target_list in os.listdir(in_GFW_dir):
            print("Loading {}".format(target_list))
            # strip .dat
            list_name = target_list[:-4] + "-in"
            target_list_path = os.path.join(in_GFW_dir, target_list)
            df = pd.read_csv(target_list_path)
            #print(df)
            self.target_lists_df[list_name] = df
        
        # load out GFW result
        out_GFW_dir = os.path.join(input_dir, "OutGFW/")
        for target_list in os.listdir(out_GFW_dir):
            print("Loading {}".format(target_list))
            # strip .dat
            list_name = target_list[:-4] + "-out"
            target_list_path = os.path.join(out_GFW_dir, target_list)
            df = pd.read_csv(target_list_path)
            #print(df)
            self.target_lists_df[list_name] = df
    
    def who_response(self):
        # output latex table
        print("======= WHO RESPONSE? =======")
        statistics_df = pd.DataFrame(columns=['list name', 'total', 'tcp scan', 'tcp percentage','mptcp scan', 'mptcp percentage'])
        for target,df_file in self.target_lists_df.items():
            df = self.target_lists_df[target]
            list_name = target
            total_count = len(df)
            tcp_rsp_count = (df['tcp_scan'] > 0).sum()
            mptcp_rsp_count = (df['mptcp_scan'] > 0).sum()

            rsp_dict = {}
            rsp_dict['list name'] = list_name
            rsp_dict['total'] = total_count
            rsp_dict['tcp scan'] = tcp_rsp_count
            rsp_dict['tcp percentage'] = tcp_rsp_count / total_count
            rsp_dict['tcp percentage'] = "{:.2f}\%".format(rsp_dict['tcp percentage'] * 100)
            rsp_dict['mptcp scan'] = mptcp_rsp_count
            rsp_dict['mptcp percentage'] = mptcp_rsp_count / total_count
            rsp_dict['mptcp percentage'] = "{:.2f}\%".format(rsp_dict['mptcp percentage'] * 100)

            # add to dataframe
            statistics_df = statistics_df._append(rsp_dict, ignore_index=True)
        print(statistics_df)
        statistics_df.to_csv("who_response.csv", index=False)
        # output latex table string
        print(statistics_df.to_latex(index=False))
    
    def mptcp_scan_status_table(self):
        ############################################################
        # MPTCP Scan Status Table
        # list name | compatible | support | mirror | percentage
        #
        ############################################################
        print("======= MPTCP SCAN STATUS TABLE =======")
        statistics_df = pd.DataFrame(columns=['list name', 'support', 'compatible', 'mirror', 'percentage'])
        for target,df_file in self.target_lists_df.items():
            df = self.target_lists_df[target]
            list_name = target
            compatible_count = (df['mptcp_scan'] == 2).sum()
            support_count = (df['mptcp_scan'] == 3).sum()
            mirror_count = (df['mptcp_scan'] == 1).sum()
            total_count = len(df)

            rsp_dict = {}
            rsp_dict['list name'] = list_name
            rsp_dict['compatible'] = compatible_count
            rsp_dict['support'] = support_count
            rsp_dict['mirror'] = mirror_count
            rsp_dict['percentage'] = (support_count + mirror_count + compatible_count) / total_count
            rsp_dict['percentage'] = "{:.2f}\%".format(rsp_dict['percentage'] * 100)

            # add to dataframe
            statistics_df = statistics_df._append(rsp_dict, ignore_index=True)
        
        # output latex table string
        print(statistics_df.to_latex(index=False))

    def mptcp_analysis(self):
        print("======= MPTCP ANALYSIS =======")
        # extract mptcp scan result and plot CDF
        # plot as 2x2 subplots to high resolution pdf
        fig = plt.figure(figsize=(17,6))
        fig.tight_layout()
        #fig.suptitle('MPTCP Support CDF')
        i = 0
        for target,df_file in self.target_lists_df.items():
            print("-------- {} --------".format(target))
            df = self.target_lists_df[target]
            rsp_type_dict = {}
            rsp_type_dict['1'] = (df['mptcp_scan'] == 1).sum()
            rsp_type_dict['2'] = (df['mptcp_scan'] == 2).sum()
            rsp_type_dict['3'] = (df['mptcp_scan'] == 3).sum()

            print("Mirror: {}".format(rsp_type_dict['1']))
            print("Compatible: {}".format(rsp_type_dict['2']))
            print("Support: {}".format(rsp_type_dict['3']))

            # rank analysis
            supported_df = df[df['mptcp_scan'] == 3]
            mirror_df = df[df['mptcp_scan'] == 1]
            supported_df['rank'] = supported_df.index
            mirror_df['rank'] = mirror_df.index

            print(supported_df)
            print(mirror_df)
            
            # plot to culmulative distribution function
            ax = fig.add_subplot(2,4,i+1)
            i = i + 1
            ax.set_xscale('log')
            ax.set_yscale('log')
            #ax.set_xlabel('Rank')
            #ax.set_ylabel('CDF')
            ax.set_title(target)
            ax.plot(supported_df['rank'], np.arange(len(supported_df)) / len(supported_df), label='Support')
            ax.plot(mirror_df['rank'], np.arange(len(mirror_df)) / len(mirror_df), label='Mirror')
            ax.legend()
        plt.savefig("mptcp_analysis.pdf".format(target))
        plt.close()
    
    def display_data(self):
        for target,df in self.target_lists_df.items():
            print("Target: {}".format(target))
            print(df)

def main():
    toplist_analysis = TopListAnalysis()
    toplist_analysis.load_data("./data")
    toplist_analysis.display_data()
    toplist_analysis.who_response()
    toplist_analysis.mptcp_analysis()
    toplist_analysis.mptcp_scan_status_table()

if __name__ == '__main__':
    main()