def third_party_summary(audits):
    """Reduce the impact of third-party code"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        entity = item['entity']
        transfer_size = item['transferSize']
        blocking_time = item['blockingTime']

        sub_items = item['subItems']['items']
        sub_items_list = []
        for sub_item in sub_items:
            url = sub_item['url']
            transfer_size = sub_item['transferSize']
            blocking_time = sub_item['blockingTime']
            sub_items_list.append(
                {'url': url,
                 'transfer_size': transfer_size,
                 'blocking_time': blocking_time, })
        result_list.append({
            'entity': entity,
            'transfer_size': transfer_size,
            'blocking_time': blocking_time,
            'sub_items_list': sub_items_list
        })
    return result_list


def total_byte_weight(audits):
    """Avoids enormous network payloads"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        transfer_size = item['totalBytes']
        url = item['url']
        result_list.append({'url': url, 'transfer_size': transfer_size})
    return result_list


def duplicated_javascript(audits):
    """Remove duplicate modules in JavaScript bundles"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        source = item['source']
        wasted_bytes = item['wastedBytes']
        sub_items = item['subItems']['items']
        sub_list = []
        for sub_item in sub_items:
            source_transfer_bytes = sub_item.get('sourceTransferBytes')
            url = sub_item['url']
            sub_list.append({'url': url, 'transfer_size': source_transfer_bytes})
        result_list.append({'source': source, 'wasted_bytes': wasted_bytes, 'sub_list': sub_list})
    return result_list


def non_composited_animations(audits):
    """Avoid non-composited animations"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        snippet = item.get('node', {}).get('snippet')
        sub_items = item.get('subItems', {}).get('items')
        sub_list = []
        for sub_item in sub_items:
            failure_reason = sub_item['failureReason']
            animation = sub_item['animation']
            sub_list.append({'animation': animation, 'failure_reason': failure_reason})
        result_list.append({
            'Element': snippet,
            'sub_items': sub_items,
        })
    return result_list


def critical_request_chains(audits):
    chains = audits['details']['chains']
    result_list = []
    for chain, data_chain in chains.items():
        chain_name = data_chain['request']['url']
        time = data_chain['request']['endTime'] - data_chain['request']['startTime']
        time = round(time * 1000, 3)
        children = data_chain['children']
        children_list = []
        for item, data in children.items():
            url = data['request']['url']
            transfer_size = data['request']['transferSize']
            time = data['request']['endTime'] - data['request']['startTime']
            time = round(time * 1000, 3)
            children_list.append({'url': url, 'transfer_size': transfer_size, 'time': time})
        result_list.append({'chain_name': chain_name, 'time': time, 'children_list': children_list})
    return result_list


def unused_css_rules(audits):
    """Avoid chaining critical requests"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        url = item['url']
        transfer_size = item['totalBytes']
        potential_savings = item['wastedBytes']
        result_list.append({'URL': url, 'transfer_size': transfer_size, 'potential_savings': potential_savings})
    return result_list


def modern_image_formats(audits):
    """Serve images in next-gen formats"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        snippet = item['node']['snippet']
        image_url = item['url']
        total_bytes = item['totalBytes']
        wasted_bytes = int(item['wastedBytes'])
        result_list.append({'snippet': snippet,
                            'image_url': image_url,
                            'total_bytes': total_bytes,
                            'wasted_bytes': wasted_bytes})
    return result_list


def uses_passive_event_listeners(audits):
    """Uses passive listeners to improve scrolling performance"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        url = item.get('source', {}).get('url')
        column = item.get('source', {}).get('column')
        line = item.get('source', {}).get('line')
        result_list.append({'url': url, 'column': column, 'line': line})
    return result_list


def largest_contentful_paint_element(audits):
    """Largest Contentful Paint element"""
    items = audits['details']['items']
    result = {}
    for item in items:
        if item['headings'][0]['key'] == 'node':
            elements = []
            for sub_item in item['items']:
                node_label = sub_item['node']['nodeLabel']
                snippet = sub_item['node']['snippet']
                elements.append({'node_label': node_label, 'snippet': snippet})
            result['elements'] = elements
        elif item['headings'][0]['key'] == 'phase':
            phase_list = []
            for sub_item in item['items']:
                phase = sub_item['phase']
                percent = sub_item['percent']
                timing = int(sub_item['timing'])  # msec
                phase_list.append({'phase': phase, 'percent_LCP': percent, 'timing': timing})
            result['phase_list'] = phase_list
    return result


def unsized_images(audits):
    """Image elements do not have explicit `width` and `height`"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        url = item.get('url')
        node = item.get('node', {}).get('nodeLabel')
        selector = item.get('node', {}).get('selector')
        result_list.append({'url': url, 'node': node, 'selector': selector})
    return result_list


def lcp_lazy_loaded(audits):
    """Largest Contentful Paint image was not lazily loaded"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        snippet = item.get('node', {}).get('snippet')
        selector = item.get('node', {}).get('selector')
        result_list.append({'snippet': snippet, 'selector': selector})
    return result_list


# TODO
def unminified_css(audits):
    """Minify CSS"""


def dom_size(audits):
    """Avoid an excessive DOM size"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        statistic = item['statistic']
        value = item['value'] and item['value']['value']
        node_label = item.get('node', {}).get('nodeLabel')
        snippet = item.get('node', {}).get('snippet')
        result_list.append({'statistic': statistic, 'node_label': node_label, 'snippet': snippet, 'value': value})
    return result_list


def font_display(audits):
    """All text remains visible during webfont loads"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        url = item.get('url')
        wasted_ms = round(item.get('wastedMs', 0))
        result_list.append({'url': url, 'wasted_ms': wasted_ms})
    return result_list


def uses_text_compression(audits):
    """Enable text compression"""
    items = audits['details']['items']
    result_list = []
    return result_list


def uses_rel_preload(audits):
    """Preload key requests"""
    items = audits['details']['items']
    result_list = []
    return result_list


def user_timings(audits):
    """User Timing marks and measures"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        name = item['name']
        timing_type = item.get('timingType')
        start_time = item.get('startTime')
        duration = item.get('duration')
        result_list.append({'Name': name, 'type': timing_type, 'start_time': start_time, 'duration': duration})
    return result_list


def uses_rel_preconnect(audits):
    """Preconnect to required origins"""


def unminified_javascript(audits):
    """'Minify JavaScript"""


def bootup_time(audits):
    """JavaScript execution time"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        result_list.append({
            'url': item['url'],
            'total_cpu_time': item.get('total'),
            'script_evaluation': item.get('scripting'),
            'script_parse': item.get('scriptParseCompile'),
        })
    return result_list


def uses_responsive_images(audits):
    """Properly size images"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        result_list.append({
            'URL': item['url'],
            'selector': item.get('node', {}).get('selector'),
            'resource_size': item.get('totalBytes'),
            'potential_savings': item.get('wastedBytes'),
        })
    return result_list


def render_blocking_resources(audits):
    """Eliminate render-blocking resources"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        result_list.append({
            'URL': item['url'],
            'transfer-size': item['totalBytes'],
            'potential_savings': item['wastedMs'],
        })
    return result_list


# def metrics(audits):
#     """Collects all available metrics."""
#     items = audits['details']['items'][0]
#     for k_item, v_item in items.items():
#         result = {k_item: v_item}
#         print(k_item, v_item)  # millisecond


def uses_optimized_images(audits):
    """Efficiently encode images"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        url = item.get('url')
        snippet = item.get('node', {}).get('snippet')
        total_bytes = item.get('totalBytes')
        wasted_bytes = item.get('wastedBytes')
        result_list.append({'url': url, 'snippet': snippet, 'total_bytes': total_bytes, 'wasted_bytes': wasted_bytes})
    return result_list


def no_document_write(audits):
    """Avoids `document.write()`"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        url = item.get('url')
        snippet = item.get('node', {}).get('snippet')
        total_bytes = item.get('totalBytes')
        wasted_bytes = item.get('wastedBytes')
        result_list.append({'url': url, 'snippet': snippet, 'total_bytes': total_bytes, 'wasted_bytes': wasted_bytes})
    return result_list


def third_party_facades(audits):
    """Lazy load third-party resources with facades"""
    items = audits['details']['items']


def mainthread_work_breakdown(audits):
    """Minimize main-thread work"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        group_label = item['groupLabel']
        duration = int(item['duration'])
        result_list.append({
            'category': group_label,
            'time_spent': duration,  # ms
        })
    return result_list


def unused_javascript(audits):
    """Reduce unused JavaScript"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        url = item['url']
        total_bytes = item['totalBytes']
        wasted_bytes = item['wastedBytes']
        result_list.append({
            'url': url,
            'transfer_size': total_bytes,
            'potential_savings': wasted_bytes,
        })
    return result_list


def server_response_time(audits):
    """Initial server response time was short"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        result_list.append({
            'url': item['url'],
            'timespan_ms': item['responseTime'],
        })
    return result_list


def efficient_animated_content(audits):
    """Use video formats for animated content"""
    items = audits['details']['items']


def network_server_latency(audits):
    """Server Backend Latencies"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        result_list.append({
            'origin': item['origin'],
            'server_response_time': item['serverResponseTime']
        })
    return result_list


def long_tasks(audits):
    """Avoid long main-thread tasks"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        result_list.append({
            'url': item['url'],
            'duration_ms': item['duration']
        })
    return result_list


def uses_long_cache_ttl(audits):
    """Serve static assets with an efficient cache policy"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        result_list.append({
            'url': item['url'],
            'cache_ttl_ms': item['cacheLifetimeMs'],
            'transfer_size': item['totalBytes'],
        })
    return result_list


def prioritize_lcp_image(audits):
    """Preload Largest Contentful Paint image"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        url = item['url']
        snippet = item['node']['snippet']
        wasted_ms = item['wastedMs']
        result_list.append({'url': url, 'snippet': snippet, 'potential_savings': wasted_ms})
    return result_list


def redirects(audits):
    """Avoid multiple page redirects"""
    items = audits['details']['items']


def legacy_javascript(audits):
    """Avoid serving legacy JavaScript to modern browsers"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        result_list.append({
            'url': item['url'],
            'potential_savings': item.get('wastedBytes'),
            'sub_items': item.get('subItems', {}).get('items', []),
        })
    return result_list


def viewport(audits):
    """Has a `<meta name="viewport">` tag with `width` or `initial-scale`"""
    return audits['warnings']


def offscreen_images(audits):
    """Defer offscreen images"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        url = item.get('url')
        snippet = item.get('node', {}).get('snippet')
        total_bytes = item.get('totalBytes')
        wasted_bytes = item.get('wastedBytes')
        result_list.append({'url': url, 'snippet': snippet, 'total_bytes': total_bytes, 'wasted_bytes': wasted_bytes})
    return result_list


def layout_shift_elements(audits):
    """Avoid large layout shifts"""
    items = audits['details']['items']
    result_list = []
    for item in items:
        result_list.append({
            'element': item.get('node', {}).get('snippet'),
            'cls_contribution': item.get('score'),
        })
    return result_list


def sub_function(audits):
    headings = audits['details']['headings']
    items = audits['details']['items']
    result_list = []
    for item in items:
        result = dict()
        for k in headings:
            try:
                result[k.get('label') or k.get('valueType')] = (item[k['key']], k['valueType'])
                # result[k['valueType']] = (item[k['key']], k['valueType'])
            except KeyError:
                continue
        result_list.append(result)
    return result_list


dict_audits = {
    'third-party-summary': third_party_summary,
    'total-byte-weight': total_byte_weight,
    'duplicated-javascript': duplicated_javascript,
    'non-composited-animations': non_composited_animations,
    'critical-request-chains': critical_request_chains,
    'unused-css-rules': unused_css_rules,
    'unused-javascript': unused_javascript,
    'modern-image-formats': modern_image_formats,
    'uses-passive-event-listeners': uses_passive_event_listeners,
    'largest-contentful-paint-element': largest_contentful_paint_element,
    'unsized-images': unsized_images,
    'lcp-lazy-loaded': lcp_lazy_loaded,
    # 'unminified-css': unminified_css,  # TODO
    'dom-size': dom_size,
    'font-display': font_display,
    # 'uses-text-compression': uses_text_compression,  # TODO
    # 'uses-rel-preload': uses_rel_preload,  # TODO
    'user-timings': user_timings,
    # 'uses-rel-preconnect': uses_rel_preconnect,  # TODO
    # 'unminified-javascript': unminified_javascript,  # TODO
    'uses-optimized-images': uses_optimized_images,  # TODO
    'bootup-time': bootup_time,
    'uses-responsive-images': uses_responsive_images,
    'render-blocking-resources': render_blocking_resources,
    'no-document-write': no_document_write,  # TODO
    # 'third-party-facades': third_party_facades,  # TODO
    'mainthread-work-breakdown': mainthread_work_breakdown,
    'server-response-time': server_response_time,
    # 'efficient-animated-content': efficient_animated_content,  # TODO
    'network-server-latency': network_server_latency,
    'long-tasks': long_tasks,
    'uses-long-cache-ttl': uses_long_cache_ttl,
    'prioritize-lcp-image': prioritize_lcp_image,
    # 'redirects': redirects,  # TODO
    'legacy-javascript': legacy_javascript,
    'viewport': viewport,
    'offscreen-images': offscreen_images,
    'layout-shift-elements': layout_shift_elements,


    ############################
    # if there is no function, but there is data in detail
    ############################
    'sub_function': sub_function,
}


list_audits = {
    'third-party-summary', third_party_summary,
    'total-byte-weight', total_byte_weight,
    'duplicated-javascript', duplicated_javascript,
    'non-composited-animations', non_composited_animations,
    'critical-request-chains', critical_request_chains,
    'unused-css-rules', unused_css_rules,
    'unused-javascript', unused_javascript,
    'modern-image-formats', modern_image_formats,
    'uses-passive-event-listeners', uses_passive_event_listeners,
    'largest-contentful-paint-element', largest_contentful_paint_element,
    'unsized-images', unsized_images,
    'lcp-lazy-loaded', lcp_lazy_loaded,
    # 'unminified-css': unminified_css,  # TODO
    'dom-size', dom_size,
    'font-display', font_display,
    # 'uses-text-compression': uses_text_compression,  # TODO
    # 'uses-rel-preload': uses_rel_preload,  # TODO
    'user-timings', user_timings,
    # 'uses-rel-preconnect': uses_rel_preconnect,  # TODO
    # 'unminified-javascript': unminified_javascript,  # TODO
    'uses-optimized-images', uses_optimized_images,  # TODO
    'bootup-time', bootup_time,
    'uses-responsive-images', uses_responsive_images,
    'render-blocking-resources', render_blocking_resources,
    'no-document-write', no_document_write,  # TODO
    # 'third-party-facades': third_party_facades,  # TODO
    'mainthread-work-breakdown', mainthread_work_breakdown,
    'server-response-time', server_response_time,
    # 'efficient-animated-content': efficient_animated_content,  # TODO
    'network-server-latency', network_server_latency,
    'long-tasks', long_tasks,
    'uses-long-cache-ttl', uses_long_cache_ttl,
    'prioritize-lcp-image', prioritize_lcp_image,
    # 'redirects': redirects,  # TODO
    'legacy-javascript', legacy_javascript,
    'viewport', viewport,
    'offscreen-images', offscreen_images,
    'layout-shift-elements', layout_shift_elements,


    ############################
    # if there is no function, but there is data in detail
    ############################
    'sub_function', sub_function,
}
