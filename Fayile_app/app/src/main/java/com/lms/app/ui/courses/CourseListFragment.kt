package com.lms.app.ui.courses

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.fragment.app.viewModels
import androidx.recyclerview.widget.LinearLayoutManager
import com.lms.app.databinding.FragmentCourseListBinding
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class CourseListFragment : Fragment() {

    private var _binding: FragmentCourseListBinding? = null
    private val binding get() = _binding!!
    private val viewModel: CourseViewModel by viewModels()

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentCourseListBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.rvCourses.layoutManager = LinearLayoutManager(requireContext())

        viewModel.courses.observe(viewLifecycleOwner) { list ->
            if (list.isEmpty()) {
                binding.layoutEmpty.visibility = View.VISIBLE
                binding.rvCourses.visibility = View.GONE
            } else {
                binding.layoutEmpty.visibility = View.GONE
                binding.rvCourses.visibility = View.VISIBLE
                // TODO: CourseAdapter — Phase 2
            }
        }

        viewModel.isLoading.observe(viewLifecycleOwner) { loading ->
            // ProgressBar əlavə ediləcək Phase 2-də
        }

        viewModel.error.observe(viewLifecycleOwner) { msg ->
            if (!msg.isNullOrBlank()) {
                Toast.makeText(requireContext(), msg, Toast.LENGTH_SHORT).show()
            }
        }

        viewModel.loadCourses()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
