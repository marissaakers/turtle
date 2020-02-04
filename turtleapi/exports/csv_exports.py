from flask import request, make_response
import csv
from io import StringIO

def lagoon_csv_export(query_data, features):
    string_io = StringIO()
    writer = csv.writer(string_io)

    header_row = []
    data = {}
    if 'morphometrics' in features:
        morphometrics_data = [x['morphometrics'] for y in query_data for x in y['encounters']]
        morph_features = features['morphometrics']

        if 'curved_length' in morph_features or 'all' in morph_features:
            header_row.append('curved_length')
            data['curved_length'] = [x['curved_length'] for x in morphometrics_data]

        if 'straight_length' in morph_features or 'all' in morph_features:
            header_row.append('straight_length')
            data['straight_length'] = [x['straight_length'] for x in morphometrics_data]

        if 'minimum_length' in morph_features or 'all' in morph_features:
            header_row.append('minimum_length')
            data['minimum_length'] = [x['minimum_length'] for x in morphometrics_data]

        if 'plastron_length' in morph_features or 'all' in morph_features:
            header_row.append('plastron_length')
            data['plastron_length'] = [x['plastron_length'] for x in morphometrics_data]

        if 'weight' in morph_features or 'all' in morph_features:
            header_row.append('weight')
            data['weight'] = [x['weight'] for x in morphometrics_data]

        if 'curved_width' in morph_features or 'all' in morph_features:
            header_row.append('curved_width')
            data['curved_width'] = [x['curved_width'] for x in morphometrics_data]

        if 'straight_width' in morph_features or 'all' in morph_features:
            header_row.append('straight_width')
            data['straight_width'] = [x['straight_width'] for x in morphometrics_data]

        if 'tail_length_pl_vent' in morph_features or 'all' in morph_features:
            header_row.append('tail_length_pl_vent')
            data['tail_length_pl_vent'] = [x['tail_length_pl_vent'] for x in morphometrics_data]

        if 'tail_length_pl_tip' in morph_features or 'all' in morph_features:
            header_row.append('tail_length_pl_tip')
            data['tail_length_pl_tip'] = [x['tail_length_pl_tip'] for x in morphometrics_data]

        if 'head_width' in morph_features or 'all' in morph_features:
            header_row.append('head_width')
            data['head_width'] = [x['head_width'] for x in morphometrics_data]

        if 'body_depth' in morph_features or 'all' in morph_features:
            header_row.append('body_depth')
            data['body_depth'] = [x['body_depth'] for x in morphometrics_data]

    if ('metadata' in features):
        metadata_data = [x['metadata'] for y in query_data for x in y['encounters']]

        if ('environment' in features['metadata']):
            env_features = features['metadata']['environment']
            environment_data = [x['environment'] for x in metadata_data]

            if 'water_sample' in env_features or 'all' in env_features:
                header_row.append('water_sample')
                data['water_sample'] = [x['water_sample'] for x in environment_data]

            if 'wind_speed' in env_features or 'all' in env_features:
                header_row.append('wind_speed')
                data['wind_speed'] = [x['wind_speed'] for x in environment_data]

            if 'wind_dir' in env_features or 'all' in env_features:
                header_row.append('wind_dir')
                data['wind_dir'] = [x['wind_dir'] for x in environment_data]

            if 'air_temp' in env_features or 'all' in env_features:
                header_row.append('air_temp')
                data['air_temp'] = [x['air_temp'] for x in environment_data]
            
            if 'water_temp_surface' in env_features or 'all' in env_features:
                header_row.append('water_temp_surface')
                data['water_temp_surface'] = [x['water_temp_surface'] for x in environment_data]

            if 'water_temp_1_m' in env_features or 'all' in env_features:
                header_row.append('water_temp_1_m')
                data['water_temp_1_m'] = [x['water_temp_1_m'] for x in environment_data]

            if 'water_temp_2_m' in env_features or 'all' in env_features:
                header_row.append('water_temp_2_m')
                data['water_temp_2_m'] = [x['water_temp_2_m'] for x in environment_data]

            if 'water_temp_6_m' in env_features or 'all' in env_features:
                header_row.append('water_temp_6_m')
                data['water_temp_6_m'] = [x['water_temp_6_m'] for x in environment_data]

            if 'water_temp_bottom' in env_features or 'all' in env_features:
                header_row.append('water_temp_bottom')
                data['water_temp_bottom'] = [x['water_temp_bottom'] for x in environment_data]

            if 'salinity_surface' in env_features or 'all' in env_features:
                header_row.append('salinity_surface')
                data['salinity_surface'] = [x['salinity_surface'] for x in environment_data]

            if 'salinity_1_m' in env_features or 'all' in env_features:
                header_row.append('salinity_1_m')
                data['salinity_1_m'] = [x['salinity_1_m'] for x in environment_data]

            if 'salinity_2_m' in env_features or 'all' in env_features:
                header_row.append('salinity_2_m')
                data['salinity_2_m'] = [x['salinity_2_m'] for x in environment_data]

            if 'salinity_6_m' in env_features or 'all' in env_features:
                header_row.append('salinity_6_m')
                data['salinity_6_m'] = [x['salinity_6_m'] for x in environment_data]

            if 'salinity_bottom' in env_features or 'all' in env_features:
                header_row.append('salinity_bottom')
                data['salinity_bottom'] = [x['salinity_bottom'] for x in environment_data]


    # Write header row
    writer.writerow([x for x in header_row])

    # Get the total number of encounters (and thus rows)
    rows_count = 0
    for x in query_data:
        for y in x['encounters']:
            rows_count += 1

    # Write data rows
    for row in range(0, rows_count):
        row_data = []
        for x in header_row:
            if x in data:
                row_data.append(data[x][row])
        writer.writerow(row_data)

    # Send the csv back to the user
    output = make_response(string_io.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output