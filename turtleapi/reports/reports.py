from flask import request, render_template, make_response
import requests
import json

def lagoon_report(query_data, features, report_info):
    report_data = {}

    if ('morphometrics' in features):
        morph_features = features['morphometrics']
        morphometrics_data = [x['morphometrics'] for y in query_data for x in y['encounters']]
        morphometrics = {}

        if 'curved_length' in morph_features or 'all' in morph_features:
            curved_lengths = [x['curved_length'] for x in morphometrics_data]
            morphometrics['curved_length_max'] = max(curved_lengths)
            morphometrics['curved_length_min'] = min(curved_lengths)
            morphometrics['curved_length_avg'] = sum(curved_lengths) / len(curved_lengths)

        if 'straight_length' in morph_features or 'all' in morph_features:
            straight_lengths = [x['straight_length'] for x in morphometrics_data]
            morphometrics['straight_length_max'] = max(straight_lengths)
            morphometrics['straight_length_min'] = min(straight_lengths)
            morphometrics['straight_length_avg'] = sum(straight_lengths) / len(straight_lengths)

        if 'minimum_length' in morph_features or 'all' in morph_features:
            minimum_lengths = [x['minimum_length'] for x in morphometrics_data]
            morphometrics['minimum_length_max'] = max(minimum_lengths)
            morphometrics['minimum_length_min'] = min(minimum_lengths)
            morphometrics['minimum_length_avg'] = sum(minimum_lengths) / len(minimum_lengths)

        if 'plastron_length' in morph_features or 'all' in morph_features:
            plastron_lengths = [x['plastron_length'] for x in morphometrics_data]
            morphometrics['plastron_length_max'] = max(plastron_lengths)
            morphometrics['plastron_length_min'] = min(plastron_lengths)
            morphometrics['plastron_length_avg'] = sum(plastron_lengths) / len(plastron_lengths)

        if 'weight' in morph_features or 'all' in morph_features:
            weights = [x['weight'] for x in morphometrics_data]
            morphometrics['weight_max'] = max(weights)
            morphometrics['weight_min'] = min(weights)
            morphometrics['weight_avg'] = sum(weights) / len(weights)

        if 'curved_width' in morph_features or 'all' in morph_features:
            curved_widths = [x['curved_width'] for x in morphometrics_data]
            morphometrics['curved_width_max'] = max(curved_widths)
            morphometrics['curved_width_min'] = min(curved_widths)
            morphometrics['curved_width_avg'] = sum(curved_widths) / len(curved_widths)

        if 'straight_width' in morph_features or 'all' in morph_features:
            straight_widths = [x['straight_width'] for x in morphometrics_data]
            morphometrics['straight_width_max'] = max(straight_widths)
            morphometrics['straight_width_min'] = min(straight_widths)
            morphometrics['straight_width_avg'] = sum(straight_widths) / len(straight_widths)

        if 'tail_length_pl_vent' in morph_features or 'all' in morph_features:
            tail_length_pl_vents = [x['tail_length_pl_vent'] for x in morphometrics_data]
            morphometrics['tail_length_pl_vent_max'] = max(tail_length_pl_vents)
            morphometrics['tail_length_pl_vent_min'] = min(tail_length_pl_vents)
            morphometrics['tail_length_pl_vent_avg'] = sum(tail_length_pl_vents) / len(tail_length_pl_vents)

        if 'tail_length_pl_tip' in morph_features or 'all' in morph_features:
            tail_length_pl_tips = [x['tail_length_pl_tip'] for x in morphometrics_data]
            morphometrics['tail_length_pl_tip_max'] = max(tail_length_pl_tips)
            morphometrics['tail_length_pl_tip_min'] = min(tail_length_pl_tips)
            morphometrics['tail_length_pl_tip_avg'] = sum(tail_length_pl_tips) / len(tail_length_pl_tips)

        if 'head_width' in morph_features or 'all' in morph_features:
            head_widths = [x['head_width'] for x in morphometrics_data]
            morphometrics['head_width_max'] = max(head_widths)
            morphometrics['head_width_min'] = min(head_widths)
            morphometrics['head_width_avg'] = sum(head_widths) / len(head_widths)

        if 'body_depth' in morph_features or 'all' in morph_features:
            body_depths = [x['body_depth'] for x in morphometrics_data]
            morphometrics['body_depth_max'] = max(body_depths)
            morphometrics['body_depth_min'] = min(body_depths)
            morphometrics['body_depth_avg'] = sum(body_depths) / len(body_depths)
        
        report_data['morphometrics'] = morphometrics

    if ('metadata' in features):
        metadata_data = [x['metadata'] for y in query_data for x in y['encounters']]
        metadata = {}

        # Nets
        # if ('nets' in features['metadata']):
        #     continue

        if ('environment' in features['metadata']):
            env_features = features['metadata']['environment']
            environment_data = [x['environment'] for x in metadata_data]
            environment = {}

            # Water samples are just booleans
            if 'water_sample' in env_features or 'all' in env_features:
                water_samples = [x['water_sample'] for x in environment_data]
                environment['water_sample_sum'] = sum(water_samples)
                environment['water_sample_yes'] = sum([x for x in water_samples if x == True])
                environment['water_sample_no'] = sum([x for x in water_samples if x == False])

            if 'wind_speed' in env_features or 'all' in env_features:
                wind_speeds = [x['wind_speed'] for x in environment_data]
                environment['wind_speed_max'] = max(wind_speeds)
                environment['wind_speed_min'] = min(wind_speeds)
                environment['wind_speed_avg'] = sum(wind_speeds) / len(wind_speeds)
            
            # Figure out wind_dir later

            if 'air_temp' in env_features or 'all' in env_features:
                air_temps = [x['air_temp'] for x in environment_data]
                environment['air_temp_max'] = max(air_temps)
                environment['air_temp_min'] = min(air_temps)
                environment['air_temp_avg'] = sum(air_temps) / len(air_temps)
            
            if 'water_temp_surface' in env_features or 'all' in env_features:
                water_temp_surfaces = [x['water_temp_surface'] for x in environment_data]
                environment['water_temp_surface_max'] = max(water_temp_surfaces)
                environment['water_temp_surface_min'] = min(water_temp_surfaces)
                environment['water_temp_surface_avg'] = sum(water_temp_surfaces) / len(water_temp_surfaces)

            if 'water_temp_1_m' in env_features or 'all' in env_features:
                water_temp_1_ms = [x['water_temp_1_m'] for x in environment_data]
                environment['water_temp_1_m_max'] = max(water_temp_1_ms)
                environment['water_temp_1_m_max'] = min(water_temp_1_ms)
                environment['water_temp_1_m_avg'] = sum(water_temp_1_ms) / len(water_temp_1_ms)

            if 'water_temp_2_m' in env_features or 'all' in env_features:
                water_temp_2_ms = [x['water_temp_2_m'] for x in environment_data]
                environment['water_temp_2_m_max'] = max(water_temp_2_ms)
                environment['water_temp_2_m_min'] = min(water_temp_2_ms)
                environment['water_temp_2_m_avg'] = sum(water_temp_2_ms) / len(water_temp_2_ms)

            if 'water_temp_6_m' in env_features or 'all' in env_features:
                water_temp_6_ms = [x['water_temp_6_m'] for x in environment_data]
                environment['water_temp_6_m_max'] = max(water_temp_6_ms)
                environment['water_temp_6_m_min'] = min(water_temp_6_ms)
                environment['water_temp_6_m_avg'] = sum(water_temp_6_ms) / len(water_temp_6_ms)

            if 'water_temp_bottom' in env_features or 'all' in env_features:
                water_temp_bottoms = [x['water_temp_bottom'] for x in environment_data]
                environment['water_temp_bottom_max'] = max(water_temp_bottoms)
                environment['water_temp_bottom_min'] = min(water_temp_bottoms)
                environment['water_temp_bottom_avg'] = sum(water_temp_bottoms) / len(water_temp_bottoms)

            if 'salinity_surface' in env_features or 'all' in env_features:
                salinity_surfaces = [x['salinity_surface'] for x in environment_data]
                environment['salinity_surface_max'] = max(salinity_surfaces)
                environment['salinity_surface_min'] = min(salinity_surfaces)
                environment['salinity_surface_avg'] = sum(salinity_surfaces) / len(salinity_surfaces)

            if 'salinity_1_m' in env_features or 'all' in env_features:
                salinity_1ms = [x['salinity_1_m'] for x in environment_data]
                environment['salinity_1_m_max'] = max(salinity_1_ms)
                environment['salinity_1_m_min'] = min(salinity_1_ms)
                environment['salinity_1_m_avg'] = sum(salinity_1_ms) / len(salinity_1_ms)

            if 'salinity_2_m' in env_features or 'all' in env_features:
                salinity_2_ms = [x['salinity_2_m'] for x in environment_data]
                environment['salinity_2_m_max'] = max(salinity_2_ms)
                environment['salinity_2_m_min'] = min(salinity_2_ms)
                environment['salinity_2_m_avg'] = sum(salinity_2_ms) / len(salinity_2_ms)

            if 'salinity_6_m' in env_features or 'all' in env_features:
                salinity_6_ms = [x['salinity_6_m'] for x in environment_data]
                environment['salinity_6_m_max'] = max(salinity_6_ms)
                environment['salinity_6_m_min'] = min(salinity_6_ms)
                environment['salinity_6_m_avg'] = sum(salinity_6_ms) / len(salinity_6_ms)

            if 'salinity_bottom' in env_features or 'all' in env_features:
                salinity_bottoms = [x['salinity_bottom'] for x in environment_data]
                environment['salinity_bottom_max'] = max(salinity_bottoms)
                environment['salinity_bottom_min'] = min(salinity_bottoms)
                environment['salinity_bottom_avg'] = sum(salinity_bottoms) / len(salinity_bottoms)

            metadata['environment'] = environment

        report_data['metadata'] = metadata
        

    # Make json with rendered html template
    html = render_template('reports/report_template.html', data=report_data, features=features, info=report_info)
    data = {}
    data['html'] = html
    data_json = json.dumps(data)

    # Call the other lambda function to get our pdf
    url = 'https://ksts2jkrd8.execute-api.us-east-2.amazonaws.com/dev/report'
    pdf = requests.post(url, data=data_json).content

    # Return the pdf
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response