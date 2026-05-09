package com.lms.app.ui.dashboard

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.lms.app.databinding.FragmentDashboardBinding
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class DashboardFragment : Fragment() {

    private var _binding: FragmentDashboardBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentDashboardBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // SharedPrefs-dən istifadəçi adını göstər
        val prefs = requireContext().getSharedPreferences("lms_secure_prefs", 0)
        val userName = prefs.getString("user_name", "İstifadəçi") ?: "İstifadəçi"
        val role = prefs.getString("user_role", "student") ?: "student"

        binding.tvWelcome.text = "Xoş gəldin, $userName!"
        binding.tvRole.text = if (role == "teacher") "👨‍🏫 Müəllim" else "👨‍🎓 Tələbə"
        binding.tvLessonPrice.text = "Dərs qiyməti: 25 AZN"
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

