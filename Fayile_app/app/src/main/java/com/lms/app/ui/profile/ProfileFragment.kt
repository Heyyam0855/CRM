package com.lms.app.ui.profile

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.lms.app.databinding.FragmentProfileBinding
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class ProfileFragment : Fragment() {

    private var _binding: FragmentProfileBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentProfileBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val prefs = requireContext().getSharedPreferences("lms_secure_prefs", 0)
        val name = prefs.getString("user_name", "İstifadəçi") ?: "İstifadəçi"
        val email = prefs.getString("user_email", "") ?: ""
        val role = prefs.getString("user_role", "student") ?: "student"

        binding.tvName.text = name
        binding.tvEmail.text = email
        binding.tvRole.text = if (role == "teacher") "👨‍🏫 Müəllim" else "👨‍🎓 Tələbə"

        // Çıxış düyməsi
        binding.btnLogout.setOnClickListener {
            prefs.edit().clear().apply()
            requireActivity().recreate()
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}

