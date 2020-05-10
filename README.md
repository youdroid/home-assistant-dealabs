# WIP

## Sensor Integration 
```yaml
  - platform: Dealabs
    token: !secret token
```


## Integration with markdown

```yaml
   - type: conditional
     conditions:
      - entity: sensor.dealabs
        state_not: '0'
     card:
      type: markdown
      content: |
            <table>
            {%set dealTotalNumber = states("sensor.dealabs") |int%}
            
            {%- for number in range(dealTotalNumber) -%}
            {% set dealNumber = "Alert_" + number |string %}
            {% set deal = state_attr("sensor.dealabs", dealNumber)  | from_json%}
            <tr>
                <td>
                    <a href="{{deal.link}}"><img src="{{deal.image}}"></a>
                </td>
                <td>
                   <div>{{deal.pubDate}}</div>
                   <div>{{deal.title}}</div>
                   <div>{{deal.category}} | {{deal.merchant}}</div>
                   <div>{{deal.price}}</div>
                </td>
            </tr>
            {%- endfor -%}
            </table>
```