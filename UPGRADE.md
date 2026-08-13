# V1.0 candidate upgrade

Replace the matching files in `custom_components/vasttrafik_departures/`.

This candidate adds:
- Friendly route names
- Per-route refresh intervals: 30, 60, 120 or 300 seconds
- English and Swedish entity/config translations
- Status sensor (`on_time`, `delayed`, `cancelled`) with translated states
- Numeric delay sensor
- Dashboard-ready departure board attributes
- Backward compatibility for existing routes

Existing routes continue to work. To assign a friendly route name or custom refresh interval to an old route, recreate that route for now.
