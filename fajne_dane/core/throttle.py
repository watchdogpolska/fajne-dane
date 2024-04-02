from rest_framework.throttling import UserRateThrottle


class TierBasedRateThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        user = request.user
        self.rate = '200/day'
        if user.is_authenticated:
            self.rate = '200/hour'
            if request.user.is_staff or request.user.is_superuser:
                self.rate = '1000/minute'

        self.num_requests, self.duration = self.parse_rate(self.rate)

        return super().allow_request(request, view)
