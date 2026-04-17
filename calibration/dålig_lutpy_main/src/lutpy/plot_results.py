import pandas as pd
import kaleido
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.kaleido.scope.mathjax = None

def concat_optimal_pairs():
    ge_lung_list = []
    ge_soft_list = []
    ge_bone_list = []

    siemens_lung_list = []
    siemens_soft_list = []
    siemens_bone_list = []

    for iteration in range(30):
        file_name_ge: str = r"Output\Optimal_energy\Optimal energy GE ({}).xlsx".format(iteration + 1)
        file_name_siemens: str = r"Output\Optimal_energy\Optimal energy SIEMENS ({}).xlsx".format(iteration + 1)

        ge_lung_list = collect_optimal_pairs(
            file_name_ge, "df_rmse_lung_ww", iteration, ge_lung_list)
        ge_soft_list = collect_optimal_pairs(
            file_name_ge, "df_rmse_soft_ww", iteration, ge_soft_list)
        ge_bone_list = collect_optimal_pairs(
            file_name_ge, "df_rmse_bone_ww", iteration, ge_bone_list)

        siemens_lung_list = collect_optimal_pairs(
            file_name_siemens, "df_rmse_lung_ww", iteration, siemens_lung_list)
        siemens_soft_list = collect_optimal_pairs(
            file_name_siemens, "df_rmse_soft_ww", iteration, siemens_soft_list)
        siemens_bone_list = collect_optimal_pairs(
            file_name_siemens, "df_rmse_bone_ww", iteration, siemens_bone_list)

    df_ge_lung = concat_and_sort_df(ge_lung_list)
    df_ge_soft = concat_and_sort_df(ge_soft_list)
    df_ge_bone = concat_and_sort_df(ge_bone_list)

    df_siemens_lung = concat_and_sort_df(siemens_lung_list)
    df_siemens_soft = concat_and_sort_df(siemens_soft_list)
    df_siemens_bone = concat_and_sort_df(siemens_bone_list)

    return df_ge_lung, df_ge_soft, df_ge_bone, df_siemens_lung, df_siemens_soft, df_siemens_bone


def collect_optimal_pairs(file_name, sheet, iteration, lst):
    df_temp = pd.read_excel(file_name, usecols="B:F", sheet_name=sheet, nrows=1)
    df_temp["iteration"] = iteration + 1
    lst.append(df_temp)
    return lst


def concat_and_sort_df(lst):
    df = pd.concat(lst)
    df["kev_pair"] = df["kev_low"].astype(str) + "/" + df["kev_high"].astype(str)
    df = df.sort_values(by="kev_low")
    return df


def plot_optimal_energy_histograms(df_ge_lung, df_ge_soft, df_ge_bone,
                                   df_siemens_lung, df_siemens_soft, df_siemens_bone):
    print("Time to plot Histograms!")
    fig_1 = px.histogram(df_ge_lung, x="kev_pair",
                         title="Optimal energy pairs for lung tissue on GE",
                         labels={"count": "keV pair"},
                         text_auto=True)
    fig_2 = px.histogram(df_ge_soft, x="kev_pair",
                         title="Optimal energy pairs for soft tissue on GE",
                         labels={"count": "keV pair"},
                         text_auto=True)
    fig_3 = px.histogram(df_ge_bone, x="kev_pair",
                         title="Optimal energy pairs for bone on GE",
                         labels={"count": "keV pair"},
                         text_auto=True)
    fig_4 = px.histogram(df_siemens_lung, x="kev_pair",
                         title="Optimal energy pairs for lung tissue on Siemens",
                         labels={"count": "keV pair"},
                         text_auto=True)
    fig_5 = px.histogram(df_siemens_soft, x="kev_pair",
                         title="Optimal energy pairs for soft tissue on Siemens",
                         labels={"count": "keV pair"},
                         text_auto=True)
    fig_6 = px.histogram(df_siemens_bone, x="kev_pair",
                         title="Optimal energy pairs for bone on Siemens",
                         labels={"count": "keV pair"},
                         text_auto=True)
    print("So...?")
    fig_1.show()
    fig_2.show()
    fig_3.show()
    fig_4.show()
    fig_5.show()
    fig_6.show()
    #pio.write_image(fig_1, "Output/GE_lung.png", engine='kaleido')
    #fig_1.write_image("Output/Optimal_energy/plots/optimal_energy_histograms/GE lung.pdf")

    # fig_2.write_image("Output/Optimal_energy/plots/optimal_energy_histograms/GE soft.pdf")
    # fig_3.write_image("Output/Optimal_energy/plots/optimal_energy_histograms/GE bone.pdf")
    # fig_4.write_image("Output/Optimal_energy/plots/optimal_energy_histograms/Siemens lung.pdf")
    # fig_5.write_image("Output/Optimal_energy/plots/optimal_energy_histograms/Siemens soft.pdf")
    # fig_6.write_image("Output/Optimal_energy/plots/optimal_energy_histograms/Siemens bone.pdf")
    fig_1.show()
    print("Figures saved!")

    return


def plot_optimal_energy_scatter_plots(df_ge_lung, df_ge_soft, df_ge_bone,
                                      df_siemens_lung, df_siemens_soft, df_siemens_bone):
    for iteration in range(30):
        print(iteration)
        file_name_ge: str = r"Output\Optimal_energy\Optimal energy GE ({}).xlsx".format(iteration + 1)
        file_name_siemens: str = r"Output\Optimal_energy\Optimal energy SIEMENS ({}).xlsx".format(iteration + 1)

        create_scatter_plots(file_name_ge)
        create_scatter_plots(file_name_siemens, iteration)
    return


def create_scatter_plots(file_name, iteration):
    rmse_threshold_lung = 0.1
    rmse_threshold_soft = 0.01
    rmse_threshold_bone = 0.02

    if "GE" in file_name:
        manufacturer="GE"
    else:
        manufacturer="Siemens"

    df_lung_sheet_head = pd.read_excel(file_name, usecols="B:F", sheet_name="df_rmse_lung_ww")
    df_soft_sheet_head = pd.read_excel(file_name, usecols="B:F", sheet_name="df_rmse_soft_ww")
    df_bone_sheet_head = pd.read_excel(file_name, usecols="B:F", sheet_name="df_rmse_bone_ww")
    df_lung_sheet_body = pd.read_excel(file_name, usecols="B:F", sheet_name="df_rmse_lung_ww")
    df_soft_sheet_body = pd.read_excel(file_name, usecols="B:F", sheet_name="df_rmse_soft_ww")
    df_bone_sheet_body = pd.read_excel(file_name, usecols="B:F", sheet_name="df_rmse_bone_ww")

    df_lung_sheet_head = df_lung_sheet_head[df_lung_sheet_head["rmse_head"] < rmse_threshold_lung]
    df_lung_sheet_body = df_lung_sheet_body[df_lung_sheet_body["rmse_body"] < rmse_threshold_lung]
    df_soft_sheet_head = df_soft_sheet_head[df_soft_sheet_head["rmse_head"] < rmse_threshold_soft]
    df_soft_sheet_body = df_soft_sheet_body[df_soft_sheet_body["rmse_body"] < rmse_threshold_soft]
    df_bone_sheet_head = df_bone_sheet_head[df_bone_sheet_head["rmse_head"] < rmse_threshold_bone]
    df_bone_sheet_body = df_bone_sheet_body[df_bone_sheet_body["rmse_body"] < rmse_threshold_bone]

    df_lung_sheet_head["phantom"] = "head"
    df_lung_sheet_body["phantom"] = "body"
    df_soft_sheet_head["phantom"] = "head"
    df_soft_sheet_body["phantom"] = "body"
    df_bone_sheet_head["phantom"] = "head"
    df_bone_sheet_body["phantom"] = "body"

    df_lung_sheet_head["size"] = 7.5
    df_lung_sheet_body["size"] = 15
    df_soft_sheet_head["size"] = 7.5
    df_soft_sheet_body["size"] = 15
    df_bone_sheet_head["size"] = 7.5
    df_bone_sheet_body["size"] = 15

    df_lung_sheet_head["color"] = "orangered"
    df_lung_sheet_body["color"] = "royalblue"
    df_soft_sheet_head["color"] = "orangered"
    df_soft_sheet_body["color"] = "royalblue"
    df_bone_sheet_head["color"] = "orangered"
    df_bone_sheet_body["color"] = "royalblue"

    df_lung_conc = pd.concat([df_lung_sheet_body, df_lung_sheet_head])
    df_soft_conc = pd.concat([df_soft_sheet_body, df_soft_sheet_head])
    df_bone_conc = pd.concat([df_bone_sheet_body, df_bone_sheet_head])

    fig_1 = go.Figure(data=go.Scatter(
        x=df_lung_conc["kev_low"], y=df_lung_conc["kev_high"],
        mode='markers',
        marker=dict(size=df_lung_conc["size"].to_list(),
                    color=df_lung_conc["color"].to_list()),
    ))
    fig_1.update_layout(
        title="{} energy pairs with RMSE < {} for lung tissue (iteration {})".format(
            manufacturer,rmse_threshold_lung,iteration + 1),
        xaxis_title="kev_low",
        yaxis_title="kev_high"
    )

    fig_2 = go.Figure(data=go.Scatter(
        x=df_soft_conc["kev_low"], y=df_soft_conc["kev_high"],
        mode='markers',
        marker=dict(size=df_soft_conc["size"].to_list(),
                    color=df_soft_conc["color"].to_list()),
    ))
    fig_2.update_layout(
        title="{} energy pairs with RMSE < {} for soft tissue (iteration {})".format(
            manufacturer,rmse_threshold_lung,iteration + 1),
        xaxis_title="kev_low",
        yaxis_title="kev_high"
    )

    fig_3 = go.Figure(data=go.Scatter(
        x=df_bone_conc["kev_low"], y=df_bone_conc["kev_high"],
        mode='markers',
        marker=dict(size=df_bone_conc["size"].to_list(),
                    color=df_bone_conc["color"].to_list()),
    ))
    fig_3.update_layout(
        title="{} energy pairs with RMSE < {} for bone tissue (iteration {})".format(
            manufacturer,rmse_threshold_lung, iteration + 1),
        xaxis_title="kev_low",
        yaxis_title="kev_high"
    )

    fig_1.write_image("Output/Optimal_energy/plots/GE lung.pdf")
    fig_2.write_image("Output/Optimal_energy/plots/GE soft.pdf")
    fig_3.write_image("Output/Optimal_energy/plots/GE bone.pdf")

    return
